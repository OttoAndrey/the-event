from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .models import Application, Participant


class ApplicationSerializer(Serializer):
    contact_phone = CharField()
    ticket_type = CharField()

    def validate_ticket_type(self, value):
        if value not in ['standard-access', 'pro-access', 'premium-access']:
            raise ValidationError('Wrong value!')
        return value


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
