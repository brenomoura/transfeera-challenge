import uuid
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

from receivers.domain.validators import validate_email, \
    validate_cpf_cnpj, validate_pix


class PixKeyTypes(str, Enum):
    CPF = 'CPF'
    CNPJ = 'CNPJ'
    EMAIL = 'EMAIL'
    TELEFONE = 'TELEFONE'
    CHAVE_ALEATORIA = 'CHAVE_ALEATORIA'


class ReceiverStatuses(str, Enum):
    VALIDATED = "VALIDATED"
    DRAFT = "DRAFT"


class ReceiverPIX(BaseModel):
    pix_key_type: PixKeyTypes
    pix_key: str

    @model_validator(mode="after")
    def validate_pix_info(self):
        validate_pix(self.pix_key, self.pix_key_type)
        return self


class Receiver(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str
    cpf_cnpj: str
    email: Optional[str]
    status: ReceiverStatuses = ReceiverStatuses.DRAFT
    pix: ReceiverPIX

    @field_validator("email")
    def validate_email(cls, value: str | None) -> str | None:
        return validate_email(value) if value else value

    @field_validator("cpf_cnpj")
    def validate_cpf_cnpj(cls, value: str) -> str:
        return validate_cpf_cnpj(value)
