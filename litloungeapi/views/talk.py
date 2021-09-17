"""View for information about book talks"""
from django.contrib.auth.models import User
from rest_framework.permissions import DjangoModelPermissions
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from litloungeapi.models import Talk, Reader, Work

class TalkView(ViewSet):

    # permission_classes = [ DjangoModelPermissions ]
    # queryset = Talk.objects.none()    

    @action(methods=['post', 'delete'], detail=True)
    def signup(self, request, pk=None):
            reader = Reader.objects.get(user=request.auth.user)

            try:
                talk =Talk.objects.get(pk=pk) 
            except Talk.DoesNotExist:
                    return Response(
                        {'message': 'Talk does not exist.'},
                        status=status.HTTP_404_NOT_FOUND
                    )

            if request.method == "POST":
                try:
                    talk.participants.add(reader)
                    return Response({}, status=status.HTTP_201_CREATED)
                except Exception as ex:
                    return Response({'message': ex.args[0]})

            elif request.method == "DELETE":
                try: 
                    talk.attendees.remove(reader)
                    return Response(None, status=status.HTTP_204_NO_CONTENT)
                except Exception as ex:
                    return Response({'message': ex.args[0]})
            
    
    def create(self, request):

        """May need to add actions for participants"""

        """Post Operation for new talk"""
        reader = Reader.objects.get(user=request.auth.user)

        talk = Talk()
        talk.title = request.data['title']
        talk.date = request.data['date']
        talk.time = request.data['time']
        talk.description = request.data['description']
        talk.sup_materials = request.data['supMaterials']
        talk.zoom_meeting_id = request.data['zoomMeetingId']
        talk.zoom_meeting_password = request.data['zoomMeetingPassword']
        talk.host = reader

        work = Work.objects.get(pk=request.data['workId'])
        talk.work = work

        participants = request.data['participantIds']

        try:
            talk.save()
            talk.participants.set(participants)
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
            return Response(serializer.data)
            
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
        talk.sup_materials = request.data['supMaterials']
        talk.zoom_meeting_id = request.data['zoomMeetingId']
        talk.zoom_meeting_password = request.data['zoomMeetingPassword']
        talk.host = reader

        work = Work.objects.get(pk=request.data['workId'])
        talk.work = work

        participants = request.data['participantIds']
        talk.participants.set(participants)

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
            talk.joined = reader in talk.participants.all()

        work = self.request.query_params.get("workId", None)
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
    user = TalkUserSerializer(many=False)
    class Meta:
        model = Reader
        fields = ['user', 'bio']

class WorkSerializer(serializers.ModelSerializer):
    posted_by = TalkReaderSerializer(many=False)
    class Meta:
        model = Work
        fields = ('id', 'title', 'author', 'work_type', "identifier", "url_link", "description", "posted_by", "genres")
        depth = 2

class TalkSerializer(serializers.ModelSerializer):
    host = TalkReaderSerializer(many=False)
    work = WorkSerializer(many=False)

    class Meta:
        model = Talk
        fields = ('id', 'host', 'work', 'date', 'time', 'description', 'title', 'sup_materials', 'zoom_meeting_id', 'zoom_meeting_password', 'participants')
        depth = 2