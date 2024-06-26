from receivers.domain.entities import Receiver, ReceiverPIX
from receivers.infra.django_ninja_app.models import ReceiverModel


class LoadEntityException(Exception): ...


class LoadModelException(Exception): ...


class ReceiverModelMapper:
    """
    Convert the Receiver Django Model to the main entity. It also converts the Receiver Django Model back to entity
    """

    @staticmethod
    def to_entity(model: ReceiverModel) -> Receiver:
        try:
            return Receiver(
                id=model.id,
                name=model.name,
                email=model.email,
                cpf_cnpj=model.cpf_cnpj,
                status=model.status,
                pix=ReceiverPIX(pix_key_type=model.pix_key_type, pix_key=model.pix_key),
            )
        except:
            raise LoadEntityException()

    @staticmethod
    def to_model(entity: Receiver) -> ReceiverModel:
        try:
            return ReceiverModel(
                id=entity.id,
                name=entity.name,
                email=entity.email,
                cpf_cnpj=entity.cpf_cnpj,
                pix_key_type=entity.pix.pix_key_type.value,
                pix_key=entity.pix.pix_key,
                status=entity.status.value,
            )
        except:
            raise LoadModelException()
