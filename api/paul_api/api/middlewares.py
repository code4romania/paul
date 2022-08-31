from django.db import connection


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
        print("Page render: {:.2f} sec for {} queries".format(sqltime, len(connection.queries)))

        return response
