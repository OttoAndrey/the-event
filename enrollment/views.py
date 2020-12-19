from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from .models import Application, Participant


class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ['contact_phone', 'ticket_type']


@api_view(['POST'])
def enroll(request):
    serializer = ApplicationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    participants = request.data.get('participants', [])  # TODO validate data!

    application = Application.objects.create(
        contact_phone=str(request.data['contact_phone']),
        ticket_type=str(request.data['ticket_type']),
    )

    participants = [Participant(application=application, **fields) for fields in participants]
    Participant.objects.bulk_create(participants)

    return Response({
        'application_id': application.id,
    })
