from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "hello/home.html", {})

