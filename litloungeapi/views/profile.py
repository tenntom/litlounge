"""View for profile information"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
#from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from litloungeapi.models import Talk, Reader, Work


class Profile(ViewSet):
    """Gamer can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource"""

        reader = Reader.objects.get(user=request.auth.user)
        talks = Talk.objects.filter(participants=reader)
        host_talks = Talk.objects.filter(host=reader)

        talks = TalkSerializer(
            talks, many=True, context={'request': request})
        host_talks = TalkSerializer(
            host_talks, many=True, context={'request': request})
        reader = ReaderSerializer(
            reader, many=False, context={'request': request})

        profile = {}
        profile["reader"] = reader.data
        profile["talks"] = talks.data
        profile["host_talks"] = host_talks.data

        return Response(profile)



class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('title', 'author')


class TalkSerializer(serializers.ModelSerializer):
    work = WorkSerializer(many=False)

    class Meta:
        model = Talk
        fields = ('id', 'host', 'work', 'date', 'time','title', 'participants', 'joined')
        depth = 2

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class ReaderSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Reader
        fields = ('user', 'bio', 'genres')
        depth = 2