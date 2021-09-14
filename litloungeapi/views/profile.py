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

        talks = TalkSerializer(
            talks, many=True, context={'request': request})
        reader = ReaderSerializer(
            reader, many=False, context={'request': request})

        # Manually construct the JSON structure you want in the response
        profile = {}
        profile["reader"] = reader.data
        profile["events"] = talks.data

        return Response(profile)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class ReaderSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Reader
        fields = ('user', 'bio')


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('title', 'author')


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    work = WorkSerializer(many=False)

    class Meta:
        model = Talk
        fields = ('id', 'game', 'description', 'date', 'time')

class TalkSerializer(serializers.ModelSerializer):
    work = WorkSerializer(many=False)

    class Meta:
        model = Talk
        fields = ('id', 'host', 'work', 'date', 'time','title', 'participants')
        depth = 2