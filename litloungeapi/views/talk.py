"""View for informaiton about book talks"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from litloungeapi.models import Talk, Reader, Work

class TalkView(ViewSet):
    
    def create(self, request):

        """May need to add actions for attendees"""

        """Post Operation for new talk"""
        reader = Reader.objects.get(user=request.auth.user)

        talk = Talk()
        talk.title = request.data['title']
        talk.date = request.data['date']
        talk.time = request.data['time']
        talk.description = request.data['description']
        talk.sup_materials = request.data['sup_materials']
        talk.zoom_meeting_id = request.data['zoom_meeting_id']
        talk.zoom_meeting_password = request.data['zoom_meeting_password']
        talk.host = reader

        work = Work.objects.get(pk=request.data['workId'])
        talk.work = work

        try:
            talk.save()
            serializer = TalkSerializer(talk, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message},
            status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle requests for single talks"""
        try:
            talk= Talk.objects.get(pk=pk)
            serializer = TalkSerializer(talk, context={'request': request})
            return(serializer)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle Put requests"""
        reader = Reader.objects.get(user=request.auth.user)

        talk = Talk.objects.get(pk=pk)
        talk.title = request.data['title']
        talk.date = request.data['date']
        talk.time = request.data['time']
        talk.description = request.data['description']
        talk.sup_materials = request.data['sup_materials']
        talk.zoom_meeting_id = request.data['zoom_meeting_id']
        talk.zoom_meeting_password = request.data['zoom_meeting_password']
        talk.host = reader

        work = Work.objects.get(pk=request.data['workId'])
        talk.work = work
        talk.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Hanlde Delete Requests"""
        try:
            talk = Talk.objects.get(pk=pk)
            talk.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Talk.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Gets all talks"""
        reader = Reader.objects.get(user=request.auth.user)
        talks = Talk.objects.all()

        for talk in talks:
            talk.joined = reader in talk.attendees.all()

        work = self.request.query_params.get("work_id", None)
        if work is not None:
            talks = talks.filter(work__id=work)

        serializer = TalkSerializer(
            talks, many=True, context={'request': request})

        return Response(serializer.data)


"""Serializers"""

class TalkUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class TalkReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = ['user', 'bio']

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('id', 'title', 'author', 'media_type', "identifier", "url_link", "description", "post_by", "genres")

class TalkSerializer(serializers.ModelSerializer):
    host = TalkUserSerializer(many=False)
    work = WorkSerializer(many=False)

    class Meta:
        model = Talk
        fields = ('id', 'host', 'date', 'time', 'description', 'title', 'sup_materials', 'zoom_meeting_id', 'zoom_meeting_password', 'participants')