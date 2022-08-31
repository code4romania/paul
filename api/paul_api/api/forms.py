from copy import deepcopy

from django.forms import (
    BooleanField,
    CharField,
    ChoiceField,
    DateTimeField,
    FloatField,
    IntegerField,
    ModelForm,
)
from django.utils.translation import ugettext_lazy as _

from .validators import (
    validate_text,
    validate_float,
    validate_int,
    validate_date,
    validate_bool,
    validate_enum,
)
from datetime import datetime


class BaseDynamicEntityForm(ModelForm):
    """
    ``ModelForm`` for entity with support for EAV attributes. Form fields are
    created on the fly depending on schema defined for given entity instance.
    If no schema is defined (i.e. the entity instance has not been saved yet),
    only static fields are used. However, on form validation the schema will be
    retrieved and EAV fields dynamically added to the form, so when the
    validation is actually done, all EAV fields are present in it (unless
    Rubric is not defined).

    Mapping between attribute types and field classes is as follows:

    =====  =============
    Type      Field
    =====  =============
    text   CharField
    float  IntegerField
    int    DateTimeField
    bool   BooleanField
    enum   ChoiceField
    =====  =============
    """

    FIELD_CLASSES = {
        "text": CharField,
        "float": FloatField,
        "int": IntegerField,
        "date": DateTimeField,
        "bool": BooleanField,
        "enum": ChoiceField,
    }

    DATATYPE_VALIDATORS = {
        "text": validate_text,
        "float": validate_float,
        "int": validate_int,
        "date": validate_date,
        "bool": validate_bool,
        "enum": validate_enum,
    }

    def __init__(self, data=None, *args, **kwargs):
        super(BaseDynamicEntityForm, self).__init__(data, *args, **kwargs)
        # config_cls = self.instance._eav_config_cls
        # self.entity = getattr(self.instance, config_cls.eav_attr)
        self._build_dynamic_fields()

    def _build_dynamic_fields(self):
        # Reset form fields.
        self.fields = deepcopy(self.base_fields)

        for attribute in self.instance.table.fields.all():
            value = self.instance.data[attribute.name]
            datatype = attribute.field_type
            defaults = {
                "label": attribute.name.capitalize(),
                # 'required': False,
                "required": attribute.required,
                "help_text": attribute.help_text,
                "validators": [self.DATATYPE_VALIDATORS[datatype]],
            }

            if datatype == "enum":
                values = [(x, x) for x in attribute.choices]
                choices = [("", "-----")] + values
                defaults.update({"choices": choices})

                if value:
                    defaults.update({"initial": value})

            elif datatype == "date":
                value = datetime.fromisoformat(value)
                # defaults.update({'widget': AdminSplitDateTime})

            MappedField = self.FIELD_CLASSES[datatype]
            # self.fields[attribute.name] = MappedField(**defaults)
            self.fields[attribute.name] = MappedField(**defaults)
            # Fill initial data (if attribute was already defined).
            if value:
                self.initial[attribute.name] = value

    def save(self, commit=True):
        """
        Saves this ``form``'s cleaned_data into model instance
        """
        print("SAVE inainte errors")
        if self.errors:
            raise ValueError(
                _("The %s could not be saved because the data didn't validate." % self.instance._meta.object_name)
            )

        # Create entity instance, don't save yet.
        print("SAVE")
        print("SAVE")
        instance = super(BaseDynamicEntityForm, self).save(commit=False)
        print("SAVE")
        print("SAVE")
        print("SAVE")
        print("SAVE")
        # Assign attributes.
        for attribute in instance.table.fields.all():
            value = self.cleaned_data.get(attribute.name)
            print(attribute.name, value)

            instance.data[attribute.name] = value

        # Save entity and its attributes.
        if commit:
            instance.save()
            # self._save_m2m()

        return instance
