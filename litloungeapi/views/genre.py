"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
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


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'label')