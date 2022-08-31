from django.db.models import (
    Q, Count, Sum, Min, Max, Avg, StdDev,
    DateTimeField, DateField, CharField, FloatField, IntegerField)
from django.db.models.functions import Trunc, Cast
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.postgres.fields.jsonb import KeyTextTransform

from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_guardian.filters import ObjectPermissionsFilter

from guardian.shortcuts import get_objects_for_user
from guardian.core import ObjectPermissionChecker

from rest_framework import filters as drf_filters
from django_filters import rest_framework as filters
from rest_framework_tricks.filters import OrderingFilter



import csv
import json
from io import StringIO
import os
from datetime import datetime

from api import serializers, models
from . import permissions as api_permissions
from .permissions import BaseModelPermissions
from . import utils
from pprint import pprint


class EntriesPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "perPage"
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.users.UserListSerializer
    pagination_class = EntriesPagination

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.users.UserCreateSerializer
        elif self.action == "retrieve":
            return serializers.users.UserDetailSerializer
        elif self.action in ["update","partial_update"]:
            return serializers.users.UserUpdateSerializer
        return serializers.users.UserListSerializer

    def get_queryset(self):
        user = self.request.user
        ordering = self.request.GET.get('__order', 'id')

        if 'admin' in user.groups.values_list('name', flat=True):
            return User.objects.all().order_by(ordering)
        return User.objects.filter(pk=user.pk)

    @action(
        detail=True,
        methods=["get"],
        name="Toggle user activation",
        url_path="toggle-activation"
    )
    def toggle_activation(self, request, pk):
        request_user = request.user
        user = self.get_object()
        if 'admin' in request_user.groups.values_list('name', flat=True):
            user.is_active = not user.is_active
            user.save()
        response = serializers.users.UserDetailSerializer(
            user, context={'request': request})
        return Response(response.data)


class UserView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        user = request.user
        profile = user.userprofile
        profile_cards = [card.card for card in profile.dashboard_cards.all()]
        admin_group = Group.objects.get(name='admin')

        cards_serializer = serializers.cards.ListSerializer(
            profile_cards, many=True, context={'request': request})
        charts_serializer = serializers.charts.ListSerializer(
            user.userprofile.dashboard_charts.all(), many=True, context={'request': request})
        filters_serializer = serializers.filters.FilterListSerializer(
            user.userprofile.dashboard_filters.all(), many=True, context={'request': request})

        dashboard = {
            "cards": cards_serializer.data,
            "charts": charts_serializer.data,
            "filters": filters_serializer.data
        }

        response = {
            "username": user.username,
            "id": user.id,
            "dashboard": dashboard,
            "is_admin": admin_group in user.groups.all(),
            "avatar": request.build_absolute_uri(profile.avatar.url) if profile.avatar else None
        }
        return Response(response)


class DatabaseViewSet(viewsets.ModelViewSet):
    queryset = models.Database.objects.all()
    serializer_class = serializers.databases.DatabaseSerializer


class CanView(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `user`.
        return obj.owner == request.user


class MyFilterBackend(filters.DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        # merge filterset kwargs provided by view class
        if hasattr(view, "get_filterset_kwargs"):
            kwargs.update(view.get_filterset_kwargs())

        return kwargs


class TableViewSet(viewsets.ModelViewSet):
    queryset = models.Table.objects.all().prefetch_related("fields").select_related("database").order_by("id")
    pagination_class = EntriesPagination
    # permission_classes = (BaseModelPermissions, api_permissions.IsAuthenticatedOrGetToken )
    permission_classes = [BaseModelPermissions]
    filter_backends = [ObjectPermissionsFilter]
    # filterset_fields = ["active"]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.databases.DatabaseTableListSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return serializers.tables.TableCreateSerializer
        return serializers.tables.TableSerializer

    def get_permissions(self):
        base_permissions = super(self.__class__, self).get_permissions()
        if self.action == "csv_export":
            base_permissions = (api_permissions.IsAuthenticatedOrGetToken(),)
        return base_permissions

    def create(self, request):
        fields = request.data.get("fields")
        csv_import_pk = request.data.get("import_id")
        data = request.data
        serializer = serializers.tables.TableCreateSerializer(
            data=data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        if not csv_import_pk:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        table = models.Table.objects.get(pk=serializer.data["id"])
        csv_import = models.CsvImport.objects.get(pk=csv_import_pk)

        for field in fields:
            table_column, _ = models.TableColumn.objects.get_or_create(
                table=table,
                name=utils.snake_case(field["display_name"]),
                display_name=field["display_name"],
                field_type=field["field_type"],
            )
            csv_field_map = models.CsvFieldMap.objects.create(
                table=table,
                original_name=field["original_name"],
                display_name=field["display_name"],
                field_type=field["field_type"],
                field_format=field["field_format"],
                table_column=table_column
            )
            table_column.required = field.get('required', False)
            table_column.unique = field.get('unique', False)
            table_column.save()
            csv_field_map.required = field.get('required', False)
            csv_field_map.unique = field.get('unique', False)
            csv_field_map.save()

        try:
            file_content = csv_import.file.read().decode("utf-8")
        except:
            csv_import.file.seek(0)
            file_content = csv_import.file.read().decode("windows-1252")
        decoded_file = file_content.splitlines()
        if not csv_import.delimiter:
            csv_import.file.seek(0)
            dialect = csv.Sniffer().sniff(file_content[:2000])
            reader = csv.DictReader(decoded_file, delimiter=dialect.delimiter)
        else:
            reader = csv.DictReader(decoded_file, delimiter=csv_import.delimiter)

        errors, errors_count, import_count_created, import_count_updated = utils.import_csv(reader, table)
        csv_import.errors = errors
        csv_import.errors_count = errors_count
        csv_import.import_count_created = import_count_created
        csv_import.import_count_updated = import_count_updated
        csv_import.table = table
        csv_import.save()
        response = {
            "errors_count": errors_count,
            "import_count_created": import_count_created,
            "import_count_updated": import_count_updated,
            "errors": errors,
            "id": table.id,
        }
        return Response(response)

    @action(
        detail=True,
        methods=["post"],
        name="CSV manual import view",
        url_path="csv-manual-import",
    )
    def csv_manual_import(self, request, pk):
        fields = request.data.get("fields")
        csv_import_pk = request.data.get("import_id")

        table = self.get_object()
        csv_import = models.CsvImport.objects.get(pk=csv_import_pk)

        for field in fields:
            csv_field_map= models.CsvFieldMap.objects.get(
                csv_import=csv_import,
                original_name=field["original_name"]
            )
            csv_field_map.field_format=field["field_format"]
            csv_field_map.unique=field["unique"]

            csv_field_map.required=field["required"]

            if field["table_field"]:
                csv_field_map.table_column_id=field["table_field"]

            csv_field_map.save()


        try:
            file_content = csv_import.file.read().decode("utf-8")
        except:
            csv_import.file.seek(0)
            file_content = csv_import.file.read().decode("windows-1252")
        decoded_file = file_content.splitlines()
        if not csv_import.delimiter:
            csv_import.file.seek(0)
            dialect = csv.Sniffer().sniff(file_content[:2000])
            reader = csv.DictReader(decoded_file, delimiter=dialect.delimiter)
        else:
            reader = csv.DictReader(decoded_file, delimiter=csv_import.delimiter)


        errors, errors_count, import_count_created, import_count_updated = utils.import_csv(reader, table, csv_import)

        csv_import.errors = errors
        csv_import.errors_count = errors_count
        csv_import.import_count_created = import_count_created
        csv_import.import_count_updated = import_count_updated
        csv_import.table = table
        csv_import.save()
        response = {
            "errors_count": errors_count,
            "import_count_created": import_count_created,
            "import_count_updated": import_count_updated,
            "errors": errors,
            "id": table.id,
            "import_id": csv_import.pk,
        }
        return Response(response)

    # @permission_classes([api_permissions.IsAuthenticatedOrGetToken])
    @action(
        detail=True,
        methods=["get"],
        name="CSV Export",
        url_path="csv-export",
    )
    def csv_export(self, request, pk):
        table = models.Table.objects.get(pk=pk)
        table_fields = {x.name: x for x in table.fields.all()}

        filter_dict = utils.request_get_to_filter(request.GET, table_fields, Q(), False)

        file_name = "{}__{}.csv".format(table.name, datetime.now().strftime("%d.%m.%Y"))
        with open("/tmp/{}".format(file_name), "w", encoding="utf-8-sig") as csv_export_file:
            writer = csv.DictWriter(
                csv_export_file,
                delimiter=",",
                quoting=csv.QUOTE_MINIMAL,
                fieldnames=table.fields.values_list("name", flat=True),
            )
            writer.writeheader()
            for row in table.entries.filter(filter_dict):
                writer.writerow(row.data)

        with open("/tmp/{}".format(file_name), "rb") as csv_export_file:
            response = HttpResponse(csv_export_file.read(), content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = 'attachment; filename="{}"'.format(file_name)
        os.remove("/tmp/{}".format(file_name))
        return response

    @action(
        detail=False,
        methods=["post"],
        name="Create from FilterView",
        url_path="from-filter",
    )
    def create_from_filter(self, request):

        table_name = request.data.get('table_name')
        filter_id = request.data.get('filter_id')

        serializer = serializers.tables.TableCreateSerializer(
            data={'database': 1, 'name': table_name},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        table = models.Table.objects.get(pk=serializer.data["id"])
        # table = models.Table.objects.get(name=table_name)

        filter = models.Filter.objects.get(pk=filter_id)
        filter_tables = [filter.primary_table] + [f for f in filter.join_tables.all()]
        for join_table in filter_tables:
            table_slug = join_table.table.slug
            for field in join_table.fields.all():
                table_column, _ = models.TableColumn.objects.get_or_create(
                    table=table,
                    name='{}_{}'.format(table_slug, field.name),
                    display_name=field.display_name,
                    field_type=field.field_type,
                    choices=field.choices,
                )

        primary_table = filter.primary_table
        primary_table_slug = primary_table.table.slug
        primary_table_join_field = primary_table.join_field.name

        secondary_table = filter.join_tables.all()[0]
        secondary_table_slug = secondary_table.table.slug
        secondary_table_join_field = secondary_table.join_field.name

        # Get all fields and display fields
        all_fields = []
        field_types = {}
        for field in primary_table.fields.all().order_by("id"):
            field_key = "{}__{}".format(primary_table.table.slug, field.name)
            all_fields.append(field_key)
            field_types[field_key] = field.field_type
        for field in secondary_table.fields.all().order_by("id"):
            field_key = "{}__{}".format(secondary_table.table.slug, field.name)
            all_fields.append(field_key)
            field_types[field_key] = field.field_type

        fields = all_fields

        primary_table_fields = []
        secondary_table_fields = []

        for field in fields:
            if field.startswith(primary_table_slug):
                primary_table_fields.append(field.replace(primary_table_slug + "__", "data__"))
            else:
                secondary_table_fields.append(field.replace(secondary_table_slug + "__", "data__"))

        secondary_table_fields.append("data__{}".format(secondary_table_join_field))

        # Create filters dict
        filter_dict = {
            primary_table_slug: {},
            secondary_table_slug: {},
        }

        # for key in filter.filters:
        #     table_field = "__".join(key.split("__")[:2])
        #     if key and table_field in all_fields:
        #         table = key.split("__")[0]
        #         field = key.replace(table + "__", "")

        #         filter_dict.setdefault(table, {})
        #         value = filter.filters.get(key).split(",")

        #         if len(value) == 1:
        #             value = value[0]
        #         else:
        #             field = field + "__in"

        #         if field_types[table_field] in [
        #             "float",
        #             "int",
        #         ]:
        #             filter_dict[table]["data__{}".format(field)] = float(value)
        #         else:
        #             filter_dict[table]["data__{}".format(field)] = value

        join_values = (
            models.Entry.objects.filter(table=primary_table.table)
            .filter(**filter_dict[primary_table_slug])
            .values("data__{}".format(primary_table_join_field))
        )

        filter_dict[secondary_table_slug]["data__{}__in".format(secondary_table_join_field)] = join_values

        result_values = (
            models.Entry.objects.filter(table__slug=secondary_table_slug)
            .filter(**filter_dict[secondary_table_slug])
            .values(*secondary_table_fields)
            .order_by("data__{}".format(secondary_table_join_field))
        )

        queryset = result_values

        if not fields:
            fields = [x.replace("data__", "{}__".format(primary_table_slug)) for x in primary_table_fields]
            fields += [x.replace("data__", "{}__".format(secondary_table_slug)) for x in secondary_table_fields]
        queryset_count = queryset.count()
        paginator = Paginator(queryset, 1000)  # Show 100 objects per page, you can choose any other value

        
        for i in paginator.page_range:  # A 1-based range iterator of page numbers, e.g. yielding [1, 2, 3, 4].
            # print("Writing page:", i)
            data = paginator.get_page(i)
            page = data.object_list

            page_join_values = [x["data__{}".format(secondary_table_join_field)] for x in page]

            filter_dict[primary_table_slug]["data__{}__in".format(primary_table_join_field)] = page_join_values
            primary_table_values = {
                x.data[primary_table_join_field]: {"data__" + key: value for key, value in x.data.items()}
                for x in models.Entry.objects.filter(table=primary_table.table)
                .filter(**filter_dict[primary_table_slug])
                .exclude(data=None)
            }
            entries = []
            for entry in page:
                final_entry = {}
                final_entry_primary_table_values = {}

                entry_primary_table_values = primary_table_values[
                    entry["data__{}".format(secondary_table_join_field)]
                ]

                for key in entry:
                    final_entry[key.replace("data__", "{}_".format(secondary_table_slug))] = entry[key]
                for key in entry_primary_table_values:
                    final_entry_primary_table_values[
                        key.replace("data__", "{}_".format(primary_table_slug))
                    ] = entry_primary_table_values[key]

                final_entry.update(final_entry_primary_table_values)
                entry = models.Entry(table=table, data=final_entry)
                entries.append(entry)
            models.Entry.objects.bulk_create(entries)
        response = {
            'id': table.id
        }
        return Response(response)


class FilterViewSet(viewsets.ModelViewSet):
    queryset = models.Filter.objects.all()
    pagination_class = EntriesPagination
    filter_backends = (OrderingFilter,)

    ordering_fields = {
        'name': 'name',
        'creation_date': 'creation_date',
        'table': 'table__name',
        'owner.username': 'owner__username'
    }

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        user_view_tables = []

        for table in get_objects_for_user(user, 'api.view_table'):
            if user.has_perm('view_table', table):
                user_view_tables.append(table)
        q = Q(
                primary_table__table__in=user_view_tables,
                join_tables__table__in=user_view_tables) | \
            Q(
                primary_table__table__in=user_view_tables,
                join_tables=None
                )
        return queryset.filter(q)

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.filters.FilterListSerializer
        elif self.action == "retrieve":
            return serializers.filters.FilterDetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return serializers.filters.FilterCreateSerializer

        return serializers.filters.FilterListSerializer

    def get_permissions(self):
        base_permissions = super(self.__class__, self).get_permissions()
        if self.action == "csv_export":
            base_permissions = (api_permissions.IsAuthenticatedOrGetToken(),)
        return base_permissions

    @action(
        detail=False,
        methods=["get"],
        url_name="all-filters",
        url_path="all",
    )
    def all(self, request):
        response = serializers.filters.FilterListSerializer(self.queryset, many=True, context={'request': request})
        return Response(response.data)

    @action(
        detail=True,
        methods=["get"],
        url_name="add-to-dashboard",
        url_path="add-to-dashboard",
    )
    def add_to_dashboard(self, request, pk):
        filter = self.get_object()
        userprofile = request.user.userprofile

        if filter in userprofile.dashboard_filters.all():
            userprofile.dashboard_filters.remove(filter)
        else:
            userprofile.dashboard_filters.add(filter)
        userprofile.save()
        return Response({'filter_in_dashboard': filter in userprofile.dashboard_filters.all()})


    @action(methods=["get"], detail=True, url_path="entries", url_name="entries")
    def entries(self, request, pk):
        obj = models.Filter.objects.filter(pk=pk).prefetch_related("primary_table", "join_tables")[0]
        str_fields = request.GET.get("__fields", "") if request else None
        str_order = request.GET.get("__order", "") if request else None

        primary_table = obj.primary_table
        primary_table_slug = primary_table.table.slug

        is_two_tables_filter = False

        if obj.join_tables.all():
            primary_table_join_field = primary_table.join_field.name
            secondary_table = obj.join_tables.all()[0]
            secondary_table_slug = secondary_table.table.slug
            secondary_table_join_field = secondary_table.join_field.name
            is_two_tables_filter = True

        # Get all fields and display fields
        all_fields = []
        field_types = {}
        for field in primary_table.fields.all().order_by("id"):
            if obj.default_fields.all():
                if field in obj.default_fields.all():
                    field_key = "{}__{}".format(primary_table.table.slug, field.name)
                    all_fields.append(field_key)
                    field_types[field_key] = field.field_type
            else:
                field_key = "{}__{}".format(primary_table.table.slug, field.name)
                all_fields.append(field_key)
                field_types[field_key] = field.field_type

        if is_two_tables_filter:
            for field in secondary_table.fields.all().order_by("id"):
                if obj.default_fields.all():
                    if field in obj.default_fields.all():
                        field_key = "{}__{}".format(secondary_table.table.slug, field.name)
                        all_fields.append(field_key)
                        field_types[field_key] = field.field_type
                else:
                    field_key = "{}__{}".format(secondary_table.table.slug, field.name)
                    all_fields.append(field_key)
                    field_types[field_key] = field.field_type

        fields = all_fields
        if str_fields:
            if str_fields == "ALL":
                fields = all_fields
            else:
                fields = str_fields.split(",") if str_fields else None

        primary_table_fields = []
        secondary_table_fields = []

        for field in fields:
            if field.startswith(primary_table_slug):
                primary_table_fields.append(field.replace(primary_table_slug + "__", "data__"))
            else:
                secondary_table_fields.append(field.replace(secondary_table_slug + "__", "data__"))

        if is_two_tables_filter:
            secondary_table_fields.append("data__{}".format(secondary_table_join_field))

        # order_table = str_order.replace("-", "").split("__")[0]
        order_table = str_order.split("__")[0]
        str_order = str_order.replace(order_table + "__", "")

        if str_order:
            if order_table.startswith("-"):
                order_table = order_table[1:]
                order_by = "-data__{}".format(str_order)
            else:
                order_by = "data__{}".format(str_order)
        else:
            order_by = "id"

        table_order_by = "id"

        # Create filters dict
        filter_dict = {
            primary_table_slug: Q(),
        }
        if is_two_tables_filter:
            filter_dict[secondary_table_slug] = Q()

        filter_dict = utils.request_get_to_filter(request.GET, field_types, filter_dict, True)

        # If filter has only primary_table
        if not is_two_tables_filter:
            if order_table == primary_table_slug:
                table_order_by = order_by
            result_values = (
                models.Entry.objects.filter(table__slug=primary_table_slug)
                .filter(filter_dict[primary_table_slug])
                .values(*primary_table_fields)
                .order_by(table_order_by)
            )
            queryset = result_values
            if not fields:
                fields = [x.replace("data__", "{}__".format(primary_table_slug)) for x in primary_table_fields]
            page = self.paginate_queryset(queryset)
            if page is not None:
                final_page = []
                for entry in page:
                    final_entry = {}
                    for key in entry:
                        final_entry[key.replace("data__", "{}__".format(primary_table_slug))] = entry[key]
                    final_page.append(final_entry)

                serializer = serializers.filters.FilterEntrySerializer(final_page, many=True, context={"fields": fields})
                return self.get_paginated_response(serializer.data)
        # If filter has secondary table
        else:
            if order_table == secondary_table_slug:
                table_order_by = order_by

            join_values = (
                models.Entry.objects.filter(table=primary_table.table)
                .filter(filter_dict[primary_table_slug])
                .values("data__{}".format(primary_table.join_field.name))
                .order_by(table_order_by)
            )

            # filter_dict[secondary_table_slug]["data__{}__in".format(secondary_table_join_field)] = join_values
            filter_dict[secondary_table_slug] = filter_dict[secondary_table_slug] & Q(
                **{"data__{}__in".format(secondary_table_join_field) :join_values})
            table_order_by = "id"
            if order_table == secondary_table_slug:
                table_order_by = order_by

            result_values = (
                models.Entry.objects.filter(table__slug=secondary_table_slug)
                .filter(filter_dict[secondary_table_slug])
                .values(*secondary_table_fields)
                .order_by(table_order_by)
            )

            queryset = result_values

            if not fields:
                fields = [x.replace("data__", "{}__".format(primary_table_slug)) for x in primary_table_fields]
                fields += [x.replace("data__", "{}__".format(secondary_table_slug)) for x in secondary_table_fields]

            page = self.paginate_queryset(queryset)

            if page is not None:
                final_page = []
                page_join_values = [x["data__{}".format(secondary_table_join_field)] for x in page]

                filter_dict[primary_table_slug] = filter_dict[primary_table_slug] & Q(
                    **{"data__{}__in".format(primary_table_join_field): page_join_values})
                # filter_dict[primary_table_slug]["data__{}__in".format(primary_table_join_field)] = page_join_values
                primary_table_values = {
                    x.data[primary_table_join_field]: {"data__" + key: value for key, value in x.data.items()}
                    for x in models.Entry.objects.filter(table=primary_table.table)
                    .filter(filter_dict[primary_table_slug])
                    .exclude(data=None)
                }

                for entry in page:
                    final_entry = {}
                    final_entry_primary_table_values = {}

                    entry_primary_table_values = primary_table_values[entry["data__{}".format(secondary_table_join_field)]]
                    for key in entry:
                        final_entry[key.replace("data__", "{}__".format(secondary_table_slug))] = entry.get(key, None)
                    final_primary_table_fields = [x.replace('{}__'.format(primary_table_slug), '') for x in fields if not x.startswith('{}_'.format(secondary_table_slug))]
                    # for key in entry_primary_table_values:

                    for key in final_primary_table_fields:
                        final_entry_primary_table_values[
                            "{}__{}".format(primary_table_slug, key)
                        ] = entry_primary_table_values.get('data__' + key, None)

                    final_entry.update(final_entry_primary_table_values)
                    final_page.append(final_entry)
                serializer = serializers.filters.FilterEntrySerializer(final_page, many=True, context={"fields": fields})
                return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=True,
        url_path="csv-export",
        url_name="csv-export")
    def csv_export(self, request, pk):
        obj = models.Filter.objects.filter(pk=pk).prefetch_related("primary_table", "join_tables")[0]
        str_fields = request.GET.get("__fields", "") if request else None
        str_order = request.GET.get("__order", "") if request else None

        primary_table = obj.primary_table
        primary_table_slug = primary_table.table.slug

        is_two_tables_filter = False

        if obj.join_tables.all():
            primary_table_join_field = primary_table.join_field.name
            secondary_table = obj.join_tables.all()[0]
            secondary_table_slug = secondary_table.table.slug
            secondary_table_join_field = secondary_table.join_field.name
            is_two_tables_filter = True

        # Get all fields and display fields
        all_fields = []
        field_types = {}
        for field in primary_table.fields.all().order_by("id"):
            if obj.default_fields.all():
                if field in obj.default_fields.all():
                    field_key = "{}__{}".format(primary_table.table.slug, field.name)
                    all_fields.append(field_key)
                    field_types[field_key] = field.field_type
            else:
                field_key = "{}__{}".format(primary_table.table.slug, field.name)
                all_fields.append(field_key)
                field_types[field_key] = field.field_type

        if is_two_tables_filter:
            for field in secondary_table.fields.all().order_by("id"):
                if obj.default_fields.all():
                    if field in obj.default_fields.all():
                        field_key = "{}__{}".format(secondary_table.table.slug, field.name)
                        all_fields.append(field_key)
                        field_types[field_key] = field.field_type
                else:
                    field_key = "{}__{}".format(secondary_table.table.slug, field.name)
                    all_fields.append(field_key)
                    field_types[field_key] = field.field_type

        fields = all_fields
        if str_fields:
            if str_fields == "ALL":
                fields = all_fields
            else:
                fields = str_fields.split(",") if str_fields else None

        primary_table_fields = []
        secondary_table_fields = []

        for field in fields:
            if field.startswith(primary_table_slug):
                primary_table_fields.append(field.replace(primary_table_slug + "__", "data__"))
            else:
                secondary_table_fields.append(field.replace(secondary_table_slug + "__", "data__"))

        if is_two_tables_filter:
            secondary_table_fields.append("data__{}".format(secondary_table_join_field))

        # order_table = str_order.replace("-", "").split("__")[0]
        order_table = str_order.split("__")[0]
        str_order = str_order.replace(order_table + "__", "")

        if str_order:
            if str_order.startswith("-"):
                order_by = "-data__{}".format(str_order[1:])
            else:
                order_by = "data__{}".format(str_order)
        else:
            order_by = "id"

        table_order_by = "id"

        if order_table == primary_table_slug:
            table_order_by = order_by

        # Create filters dict
        filter_dict = {
            primary_table_slug: Q(),
        }
        if is_two_tables_filter:
            filter_dict[secondary_table_slug] = Q()

        filter_dict = utils.request_get_to_filter(request.GET, field_types, filter_dict, True)

        # If filter has only primary_table
        if not is_two_tables_filter:
            result_values = (
                models.Entry.objects.filter(table__slug=primary_table_slug)
                .filter(filter_dict[primary_table_slug])
                .values(*primary_table_fields)
                .order_by(table_order_by)
            )
            queryset = result_values

            if not fields:
                fields = [x.replace("data__", "{}__".format(primary_table_slug)) for x in primary_table_fields]

            paginator = Paginator(queryset, 1000)  # Show 100 objects per page, you can choose any other value

            file_name = "{}__{}.csv".format(obj.slug, datetime.now().strftime("%d_%m_%Y__%H_%M"))
            with open("/tmp/{}".format(file_name), "w", encoding="utf-8-sig") as csv_export_file:
                writer = csv.DictWriter(
                    csv_export_file,
                    delimiter=",",
                    quoting=csv.QUOTE_MINIMAL,
                    fieldnames=fields,
                )
                writer.writeheader()
                for i in paginator.page_range:  # A 1-based range iterator of page numbers, e.g. yielding [1, 2, 3, 4].
                    # print("Writing page:", i)
                    data = paginator.get_page(i)
                    page = data.object_list

                    for entry in page:
                        final_entry = {}
                        final_entry_primary_table_values = {}

                        for key in entry:
                            final_entry[key.replace("data__", "{}__".format(primary_table_slug))] = entry[key]
                        
                        writer.writerow({k: v for k, v in final_entry.items() if k in fields})

        else:
            join_values = (
                models.Entry.objects.filter(table=primary_table.table)
                .filter(filter_dict[primary_table_slug])
                .values("data__{}".format(primary_table.join_field.name))
                .order_by(table_order_by)
            )

            filter_dict[secondary_table_slug] = filter_dict[secondary_table_slug] & Q(
                **{"data__{}__in".format(secondary_table_join_field): join_values})
            # filter_dict[secondary_table_slug]["data__{}__in".format(secondary_table_join_field)] = join_values

            table_order_by = "id"
            if order_table == secondary_table_slug:
                table_order_by = order_by

            result_values = (
                models.Entry.objects.filter(table__slug=secondary_table_slug)
                .filter(filter_dict[secondary_table_slug])
                .values(*secondary_table_fields)
                .order_by(table_order_by)
            )

            queryset = result_values
            if not fields:
                fields = [x.replace("data__", "{}__".format(primary_table_slug)) for x in primary_table_fields]
                fields += [x.replace("data__", "{}__".format(secondary_table_slug)) for x in secondary_table_fields]
            queryset_count = queryset.count()
            paginator = Paginator(queryset, 1000)  # Show 100 objects per page, you can choose any other value

            file_name = "{}__{}.csv".format(obj.slug, datetime.now().strftime("%d_%m_%Y__%H_%M"))
            with open("/tmp/{}".format(file_name), "w", encoding="utf-8-sig") as csv_export_file:
                writer = csv.DictWriter(
                    csv_export_file,
                    delimiter=",",
                    quoting=csv.QUOTE_MINIMAL,
                    fieldnames=fields,
                )
                writer.writeheader()
                for i in paginator.page_range:  # A 1-based range iterator of page numbers, e.g. yielding [1, 2, 3, 4].
                    # print("Writing page:", i)
                    data = paginator.get_page(i)
                    page = data.object_list

                    page_join_values = [x["data__{}".format(secondary_table_join_field)] for x in page]
                    filter_dict[primary_table_slug] = filter_dict[primary_table_slug] & Q(
                        **{"data__{}__in".format(primary_table_join_field): page_join_values})
                    # filter_dict[primary_table_slug]["data__{}__in".format(primary_table_join_field)] = page_join_values
                    primary_table_values = {
                        x.data[primary_table_join_field]: {"data__" + key: value for key, value in x.data.items()}
                        for x in models.Entry.objects.filter(table=primary_table.table)
                        .filter(filter_dict[primary_table_slug])
                        .exclude(data=None)
                    }

                    for entry in page:
                        final_entry = {}
                        final_entry_primary_table_values = {}

                        entry_primary_table_values = primary_table_values[
                            entry["data__{}".format(secondary_table_join_field)]
                        ]

                        for key in entry:
                            final_entry[key.replace("data__", "{}__".format(secondary_table_slug))] = entry[key]
                        for key in entry_primary_table_values:
                            final_entry_primary_table_values[
                                key.replace("data__", "{}__".format(primary_table_slug))
                            ] = entry_primary_table_values[key]

                        final_entry.update(final_entry_primary_table_values)
                        writer.writerow({k: v for k, v in final_entry.items() if k in fields})

        with open("/tmp/{}".format(file_name), "rb") as csv_export_file:
            # response = HttpResponse(FileWrapper(csv_export_file), content_type='application/vnd.ms-excel')
            response = HttpResponse(csv_export_file.read(), content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = 'attachment; filename="{}"'.format(file_name)
        os.remove("/tmp/{}".format(file_name))
        return response


class EntryViewSet(viewsets.ModelViewSet):
    pagination_class = EntriesPagination
    filter_backends = (drf_filters.SearchFilter,)
    serializer_class = serializers.entries.EntrySerializer
    search_fields = ["data__nume"]

    def get_queryset(self):
        return models.Entry.objects.filter(table=self.kwargs["table_pk"])

    def list(self, request, table_pk):
        table = models.Table.objects.get(pk=table_pk)
        str_fields = request.GET.get("__fields", "") if request else None
        str_order = request.GET.get("__order", "") if request else None
        table_fields = {x.name: x.field_type for x in table.fields.all().order_by("id")}
        default_fields = {x.name: x for x in table.default_fields.all().order_by("id")}

        if str_fields == "ALL":
            fields = [x for x in table_fields.keys()]
        else:
            fields = str_fields.split(",") if str_fields else None
            if not fields:
                if default_fields:
                    fields = [x for x in default_fields.keys()]
                else:
                    fields = [x for x in table_fields.keys()]


        filter_dict = utils.request_get_to_filter(request.GET, table_fields, Q(), False)

        if str_order and str_order.replace("-", "") in fields:
            if str_order.startswith("-"):
                queryset = table.entries.filter(filter_dict).order_by("-data__{}".format(str_order[1:]))
            else:
                queryset = table.entries.filter(filter_dict).order_by("data__{}".format(str_order))
        else:
            queryset = table.entries.filter(filter_dict).order_by("id")
            # queryset = table.entries.annotate(date_field=Cast(KeyTextTransform('data_iesire', "data"), DateField())).filter(date_field__exact='2020-07-21').order_by("id")

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = serializers.entries.EntrySerializer(
                page,
                many=True,
                context={"fields": fields, "table": table, "request": request},
            )
            return self.get_paginated_response(serializer.data)
        serializer = serializers.entries.EntrySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, table_pk, pk):
        table = models.Table.objects.get(pk=table_pk)
        object = models.Entry.objects.get(pk=pk)

        fields = table.fields.values_list("name", flat=True).order_by("name")
        serializer = serializers.entries.EntrySerializer(
            object,
            context={"fields": fields, "table": table, "request": request},
        )

        return Response(serializer.data)

    def update(self, request, table_pk, pk, *args, **kwargs):
        table = models.Table.objects.get(pk=table_pk)
        object = self.get_object()

        fields = table.fields.values_list("name", flat=True).order_by("name")

        serializer = serializers.entries.EntrySerializer(
            object,
            data=request.data,
            context={"fields": fields, "table": table, "request": request},
        )
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except Exception as e:
            return Response({"detail": e.detail[0]}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.data)

    def create(self, request, table_pk):
        table = models.Table.objects.get(pk=table_pk)
        data = request.data
        fields = table.fields.values_list("name", flat=True).order_by("name")

        serializer = serializers.entries.EntrySerializer(
            data=data,
            context={"fields": fields, "table": table, "request": request},
        )
        serializer.is_valid(raise_exception=False)
        try:
            self.perform_create(serializer)
        except Exception as e:
            return Response({"detail": e.detail[0]}, status=status.HTTP_409_CONFLICT)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CsvImportViewSet(viewsets.ModelViewSet):
    queryset = models.CsvImport.objects.all()
    # permission_classes = (BaseModelPermissions,)

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.csvs.CsvImportListSerializer
        return serializers.csvs.CsvImportSerializer

    def get_permissions(self):
        base_permissions = super(self.__class__, self).get_permissions()
        if self.action == "export_errors":
            base_permissions = (api_permissions.IsAuthenticatedOrGetToken(),)
        return base_permissions

    @action(
        detail=True,
        methods=["get"],
        name="Csv errors Export",
        url_path="export-errors",
    )
    def export_errors(self, request, pk):
        csv_import = self.get_object()

        file_name = "errors__" + csv_import.file.name.split("/")[-1]
        with open("/tmp/{}".format(file_name), "w", encoding="utf-8-sig") as csv_export_file:
            writer = csv.DictWriter(
                csv_export_file,
                delimiter=",",
                quoting=csv.QUOTE_MINIMAL,
                fieldnames=csv_import.errors[0]["row"].keys(),
            )
            writer.writeheader()
            for row in csv_import.errors:
                writer.writerow(row["row"])

        with open("/tmp/{}".format(file_name), "rb") as csv_export_file:
            # response = HttpResponse(FileWrapper(csv_export_file), content_type='application/vnd.ms-excel')
            response = HttpResponse(csv_export_file.read(), content_type="application/vnd.ms-excel")
            response["Content-Disposition"] = 'attachment; filename="{}"'.format(file_name)
        os.remove("/tmp/{}".format(file_name))
        return response

    def create(self, request):
        file = request.FILES["file"]
        delimiter = request.POST.get("delimiter", None)
        table_id = request.POST.get("table_id")
        if table_id:
            table = models.Table.objects.get(pk=table_id)
        fields = []

        try:
            file_content = file.read().decode("utf-8")
        except:
            try:
                file.seek(0)
                file_content = file.read().decode("windows-1252")
            except:
                response = {
                    "success": False,
                    "error_msg": 'Could not decode file',
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        decoded_file = file_content.splitlines()

        if delimiter == 'null':
            delimiter = None
        if not delimiter:
            file.seek(0)
            dialect = csv.Sniffer().sniff(file_content[:2000])
            reader = csv.DictReader(decoded_file, delimiter=dialect.delimiter)
        else:
            reader = csv.DictReader(decoded_file, delimiter=delimiter)

        csv_import = models.CsvImport.objects.create(file=file, delimiter=delimiter)

        for field in reader.fieldnames:
            csv_field_map = models.CsvFieldMap.objects.create(
                csv_import=csv_import, original_name=field, display_name=field
            )
            existing_table_field = None
            existing_table_format = None

            if table_id:
                if table.csv_field_mapping.all():
                    field_maps = table.csv_field_mapping.filter(
                        original_name=field)
                    if field_maps:
                        try:
                            existing_table_field = field_maps[0].table_column.pk
                            csv_field_map.table_column = field_maps[0].table_column
                            csv_field_map.field_format = field_maps[0].field_format
                            csv_field_map.field_type = field_maps[0].field_type
                            csv_field_map.required = field_maps[0].required
                            csv_field_map.unique = field_maps[0].unique
                            csv_field_map.save()
                        except:
                            # existing_table_field = models.TableColumn.objects.get(
                            # table=table, name=utils.snake_case(field_maps[0].field_name)).pk
                            pass
                        existing_table_format = field_maps[0].field_format
            fields.append(
                {
                    "original_name": field.encode(),
                    "display_name": field,
                    "field_type": "text",
                    "field_format": existing_table_format,
                    "table_field": existing_table_field,
                    "required": csv_field_map.required,
                    "unique": csv_field_map.unique,
                }
            )

        response = {
            "success": True,
            "import_id": csv_import.pk,
            "fields": fields,
        }
        return Response(response)


class ChartViewSet(viewsets.ModelViewSet):
    queryset = models.Chart.objects.all()
    pagination_class = EntriesPagination

    filter_backends = (OrderingFilter,)

    ordering_fields = {
        'name': 'name',
        'creation_date': 'creation_date',
        'table': 'table__name',
        'owner.username': 'owner__username'
    }

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        user_view_tables = []

        for table in get_objects_for_user(user, 'api.view_table'):
            if user.has_perm('view_table', table) or 'admin' in user.groups.values_list('name', flat=True):
                user_view_tables.append(table)
        return queryset.filter(table__in=user_view_tables)

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.charts.ListSerializer
        elif self.action == "retrieve":
            return serializers.charts.DetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return serializers.charts.CreateSerializer

    @action(
        detail=True,
        methods=["get"],
        url_name="add-to-dashboard",
        url_path="add-to-dashboard",
    )
    def add_to_dashboard(self, request, pk):
        chart = self.get_object()
        userprofile = request.user.userprofile

        if chart in userprofile.dashboard_charts.all():
            userprofile.dashboard_charts.remove(chart)
        else:
            userprofile.dashboard_charts.add(chart)
        userprofile.save()
        return Response(
            {'chart_in_dashboard': chart in userprofile.dashboard_charts.all()})

    @action(
        detail=True,
        methods=["get"],
        url_name="data",
        url_path="data",
    )
    def get_data(self, request, pk):
        chart = self.get_object()
        data = utils.get_chart_data(request, chart, chart.table)
        return Response(data)

    @action(
        detail=False,
        methods=["get"],
        url_name="preview",
        url_path="preview",
    )
    def get_preview(self, request):
        chart = models.Chart()
        table = models.Table.objects.get(pk=request.GET.get('table', None))
        timeline_field = models.TableColumn.objects.get(pk=int(request.GET.get('timeline_field', None))) if request.GET.get('timeline_field', None) else None
        x_axis_field = models.TableColumn.objects.get(pk=int(request.GET.get('x_axis_field', None))) if request.GET.get('x_axis_field', None) else None
        y_axis_field = models.TableColumn.objects.get(pk=int(request.GET.get('y_axis_field', None))) if request.GET.get('y_axis_field', None) else None
        chart.table = table
        chart.timeline_field = timeline_field
        chart.x_axis_field = x_axis_field
        chart.y_axis_field = y_axis_field

        chart.chart_type = request.GET.get('chart_type', None)
        chart.timeline_period = request.GET.get('timeline_period', None)
        chart.timeline_include_nulls = True if request.GET.get('timeline_include_nulls', None) == 'true' else False
        chart.y_axis_function = request.GET.get('y_axis_function', None)

        data = utils.get_chart_data(request, chart, table, preview=True)

        return Response(data)


class CardViewSet(viewsets.ModelViewSet):
    queryset = models.Card.objects.all()
    pagination_class = EntriesPagination
    filter_backends = (OrderingFilter,)

    ordering_fields = {
        'name': 'name',
        'creation_date': 'creation_date',
        'table': 'table__name',
        'owner.username': 'owner__username'
    }
    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        user_view_tables = []

        for table in get_objects_for_user(user, 'api.view_table'):
            if user.has_perm('view_table', table) or 'admin' in user.groups.values_list('name', flat=True):
                user_view_tables.append(table)
        return queryset.filter(table__in=user_view_tables)

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.cards.ListSerializer
        elif self.action == "retrieve":
            return serializers.cards.DetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return serializers.cards.CreateSerializer

    @action(
        detail=True,
        methods=["get"],
        url_name="add-to-dashboard",
        url_path="add-to-dashboard",
    )
    def add_to_dashboard(self, request, pk):
        card = self.get_object()
        userprofile = request.user.userprofile

        profile_card, created = models.UserCard.objects.get_or_create(
            profile=userprofile,
            card=card
            )

        if created:
            profile_card.order = userprofile.cards.count() + 1
            profile_card.save()
        else:
            profile_card.delete()

        return Response(
            {'card_in_dashboard': created})


    @action(
        detail=True,
        methods=["get"],
        url_name="data",
        url_path="data",
    )
    def get_data(self, request, pk):
        card = self.get_object()
        data = utils.get_card_data(request, card, card.table)
        return Response(data)
