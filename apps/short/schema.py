from apps.short.models import Shorting
from rest_framework import serializers


class ShortingSchema(serializers.ModelSerializer):
    class Meta:
        model = Shorting
        fields = "__all__"
