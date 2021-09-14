"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from litloungeapi.models import WorkType


class WorkTypeView(ViewSet):

    """Handles request for different types of work/ media, like books, films, etc"""

    def retrieve(self, request, pk=None):
        try:
            work_type = WorkType.objects.get(pk=pk)
            serializer = WorkTypeSerializer(work_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        work_types = WorkType.objects.all()

        serializer = WorkTypeSerializer(
            work_types, many=True, context={'request': request})
        return Response(serializer.data)


class WorkTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkType
        fields = ('id', 'label')