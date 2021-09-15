"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
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

    
    def create(self, request):

        work_type = WorkType()
        work_type.label = request.data["label"]

        try:
            work_type.save()
            serializer = WorkTypeSerializer(work_type, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):

        work_type = WorkType.objects.get(pk=pk)
        work_type.label = request.data["label"]
        work_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        try:
            work_type = WorkType.objects.get(pk=pk)
            work_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except WorkType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WorkTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkType
        fields = ('id', 'label')