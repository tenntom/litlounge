"""View module for handling requests about Works"""
from django.core.exceptions import ValidationError
from django.http.request import MediaType
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from litloungeapi.models import Work, WorkType, WorkGenre, Reader


class WorkView(ViewSet):
    """Level up Works"""
    permission_classes = [ IsAuthenticated ]
    queryset = Work.objects.none()
    def create(self, request):
        """Handle POST operations"""

        reader = Reader.objects.get(user=request.auth.user)

        work = Work()
        work.title = request.data["title"]
        work.author = request.data["author"]
        work.description = request.data["description"]
        work.identifier = request.data["identifier"]
        work.url_link = request.data["url_link"]
        work.posted_by = reader

        work_type = WorkType.objects.get(pk=request.data["workTypeId"])
        work.work_type = work_type
        
        genres = request.data["genreIds"]
        

        try:
            work.save()
            work.genres.set(genres)
            serializer = WorkSerializer(work, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Work

        Returns:
            Response -- JSON serialized Work instance
        """
        try:
            work = Work.objects.get(pk=pk)
            serializer = WorkSerializer(work, context={'request': request})
            return Response(serializer.data)

        except Work.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a Work

        Returns:
            Response -- Empty body with 204 status code
        """
        #reader = Reader.objects.get(user=request.auth.user)

        work = Work.objects.get(pk=pk)
        work.title = request.data["title"]
        work.author = request.data["author"]
        work.description = request.data["description"]
        work.identifier = request.data["identifier"]
        work.url_link = request.data["url_link"]
        work.posted_by = Reader.objects.get(pk=work.posted_by.id)
       

        work_type = WorkType.objects.get(pk=request.data["workTypeId"])
        work.work_type = work_type

        genres = request.data["genreIds"]
        work.genres.set(genres)

        work.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single Work

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            work = Work.objects.get(pk=pk)
            work.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Work.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to Works resource"""

        works = Work.objects.all()

        work_type = self.request.query_params.get('type', None)
        if work_type is not None:
            works = works.filter(work_type__id=work_type)

        serializer = WorkSerializer(
            works, many=True, context={'request': request})
        return Response(serializer.data)


class WorkSerializer(serializers.ModelSerializer):
    """JSON serializer for Works"""
    class Meta:
        model = Work
        fields = ('id', 'title', 'author', 'work_type', 'description', 'identifier', 'url_link', 'posted_by', 'genres')
        depth = 2