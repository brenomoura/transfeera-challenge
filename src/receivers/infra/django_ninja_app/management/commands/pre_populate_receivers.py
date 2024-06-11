from django.core.management.base import BaseCommand, CommandError

from receivers.domain.entities import ReceiverStatuses, PixKeyTypes
from receivers.infra.django_ninja_app.mappers import ReceiverModelMapper
from receivers.infra.django_ninja_app.models import ReceiverModel
from receivers.tests.helpers import generate_pix, new_receiver_entity


class Command(BaseCommand):
    help = "Pre populate the receivers table"
    RECEIVERS_NUMBER = 30

    def add_arguments(self, parser):
        parser.add_argument("-n", "--number", type=int, default=self.RECEIVERS_NUMBER)

    @staticmethod
    def _create_receiver_in_db(status: ReceiverStatuses = None, pix_key_type: PixKeyTypes = None) -> ReceiverModel:
        receiver = new_receiver_entity()
        if status:
            receiver.status = status
        if pix_key_type:
            receiver.pix = generate_pix(pix_key_type)
        receiver = ReceiverModelMapper.to_model(receiver)
        receiver.save()
        return receiver

    def handle(self, *args, **options):
        for idx in range(options["number"]):
            self._create_receiver_in_db()

        self.stdout.write(
            self.style.SUCCESS('Successfully created the %s receivers' % options["number"])
        )
