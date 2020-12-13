import json

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import transaction
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView

from apps.short.models import Shorting
from apps.short.schema import ShortingSchema


class ShorteningView(APIView):
    permission_classes = []

    def post(self, request):
        response = HttpResponse()
        destination = request.GET.get("destination")
        with transaction.atomic():
            try:
                URLValidator()(destination)
                shorting = (
                    Shorting.objects.filter(is_valid=False)
                    .select_for_update(skip_locked=True)
                    .first()
                )
                shorting.destination = destination
                shorting.is_valid = True
                shorting.save()
                data = ShortingSchema(shorting).data
                data["path"] = shorting.short_url
                content = {"data": data}
            except ValidationError:
                content = {"error": f"The URL format is invalid: {destination}."}

        response.content = json.dumps(content)
        return response


class IndexView(View):
    def get(self, request):
        return render(request, "index.html")


class RedirectView(View):
    def get(self, request, url_path):
        try:
            shorting = Shorting.objects.get(path=url_path)
        except Shorting.DoesNotExist:
            return HttpResponse("Page not found!", 404)

        return HttpResponseRedirect(shorting.destination)


class RedirectPreviewView(View):
    def get(self, request, url_path):
        try:
            shorting = Shorting.objects.get(path=url_path)
        except Shorting.DoesNotExist:
            return HttpResponse(f"This shortening path does not exist: {url_path}", 404)

        return HttpResponse(
            (
                f"The destination of the short URL: {shorting.short_url} is:<br><br>"
                f"<a href={shorting.destination}>{shorting.destination}</a>"
            )
        )
