from django.db import connection
from django.utils.translation import gettext_lazy as _


class SqlPrintMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        sqltime = 0  # Variable to store execution time
        for query in connection.queries:
            sqltime += float(query["time"])

        # len(connection.queries) = total number of queries
        print(
            _("Page render: {sqltime:.2f} sec for {num} queries").format(sqltime=sqltime, num=len(connection.queries))
        )

        return response
