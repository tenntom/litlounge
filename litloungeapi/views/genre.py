"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from litloungeapi.models import Genre


class GenreView(ViewSet):

    """Handles request for different types of work/ media, like books, films, etc"""

    def retrieve(self, request, pk=None):
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):

        genres = Genre.objects.all()

        serializer = GenreSerializer(
            genres, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):

        genre = Genre()
        genre.label = request.data["label"]

        try:
            genre.save()
            serializer = GenreSerializer(genre, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):

        genre = Genre.objects.get(pk=pk)
        genre.label = request.data['label']
        genre.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        try:
            genre = Genre.objects.get(pk=pk)
            genre.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'label')