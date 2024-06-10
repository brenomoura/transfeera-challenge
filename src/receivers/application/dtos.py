import uuid
from typing import Optional, List

from ninja import Schema
from pydantic import field_validator, model_validator
from typing_extensions import Self

from receivers.domain.entities import PixKeyTypes, Receiver, ReceiverPIX, \
    ReceiverStatuses
from receivers.domain.validators import validate_email, \
    validate_cpf_cnpj, validate_pix


class BaseReceiver(Schema):
    name: str
    cpf_cnpj: str
    email: Optional[str]
    pix_key_type: PixKeyTypes
    pix_key: str

    @field_validator("email")
    def validate_email(cls, value: str | None) -> str | None:
        return validate_email(value) if value else value

    @field_validator("cpf_cnpj")
    def validate_cpf_cnpj(cls, value: str) -> str:
        return validate_cpf_cnpj(value)

    @model_validator(mode="after")
    def validate_pix_info(self):
        validate_pix(self.pix_key, self.pix_key_type)
        return self

    @classmethod
    def from_entity(cls, receiver: Receiver) -> Self:
        return cls(
            name=receiver.name,
            cpf_cnpj=receiver.cpf_cnpj,
            email=receiver.email,
            pix_key_type=receiver.pix.pix_key_type,
            pix_key=receiver.pix.pix_key,
        )

    def to_entity(self) -> Receiver:
        return Receiver(
            name=self.name,
            cpf_cnpj=self.cpf_cnpj,
            email=self.email,
            pix=ReceiverPIX(
                pix_key=self.pix_key,
                pix_key_type=self.pix_key_type
            )
        )


class BaseReceiverOut(BaseReceiver):
    id: uuid.UUID
    status: ReceiverStatuses

    @classmethod
    def from_entity(cls, receiver: Receiver) -> Self:
        return cls(
            id=receiver.id,
            name=receiver.name,
            cpf_cnpj=receiver.cpf_cnpj,
            email=receiver.email,
            pix_key_type=receiver.pix.pix_key_type,
            pix_key=receiver.pix.pix_key,
            status=receiver.status,
        )


class CreateReceiverIn(BaseReceiver):
    ...


class CreateReceiverOut(BaseReceiverOut):
    ...


class UpdateReceiverIn(BaseReceiver):
    name: Optional[str]
    cpf_cnpj: Optional[str]
    email: Optional[str]
    pix_key_type: Optional[PixKeyTypes]
    pix_key: Optional[str]


class UpdateReceiverOut(BaseReceiver):
    ...


class ReceiverOut(BaseReceiverOut):
    ...


class ReceiverListOut(Schema):
    page: int
    page_size: int
    items_count: int
    results: List[ReceiverOut]


class DeleteReceiversIn(Schema):
    ids: List[uuid.UUID]


class DeleteReceiverOut(Schema):
    deleted_count: int


class Error4xxOut(Schema):
    message: str
