from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from .models import Application, Participant


class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ['contact_phone', 'ticket_type']


class ParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'email']


@api_view(['POST'])
def enroll(request):
    serializer = ApplicationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    participants = request.data.get('participants', [])
    if not isinstance(participants, list):
        raise ValidationError('Expects participants field be a list!')

    for fields in participants:
        serializer = ParticipantSerializer(data=fields)
        serializer.is_valid(raise_exception=True)

    application = Application.objects.create(
        contact_phone=str(request.data['contact_phone']),
        ticket_type=str(request.data['ticket_type']),
    )

    participants = [Participant(application=application, **fields) for fields in participants]
    Participant.objects.bulk_create(participants)

    return Response({
        'application_id': application.id,
    })
