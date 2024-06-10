import uuid
from django.db import models


# to generate the migrations run `python manage.py makemigrations receivers`

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ReceiverModel(BaseModel):
    PIX_KEY_TYPES = [
        ("CPF", "CPF"),
        ("CNPJ", "CNPJ"),
        ("EMAIL", "EMAIL"),
        ("TELEFONE", "TELEFONE"),
        ("CHAVE_ALEATORIA", "CHAVE_ALEATORIA"),
    ]
    RECEIVER_STATUS = [
        ("VALIDATED", "VALIDATED"),
        ("DRAFT", "DRAFT"),
    ]
    name = models.TextField(blank=False)
    email = models.EmailField(max_length=250, null=True, blank=False, unique=True)
    cpf_cnpj = models.CharField(max_length=14, unique=True)
    pix_key_type = models.CharField(max_length=100, choices=PIX_KEY_TYPES)
    pix_key = models.CharField(max_length=140)
    status = models.CharField(max_length=15, choices=RECEIVER_STATUS,
                              default="DRAFT")
    # the tech challenge is more related for pix, but I decided to create 
    # some columns for bank info as nullables, since the receivers list on figma
    # contains these infos
    bank_code = models.IntegerField(null=True)
    agency_code = models.CharField(null=True, max_length=11)
    account_type = models.CharField(null=True, max_length=100)
    account_code = models.CharField(null=True, max_length=12)

    class Meta:
        db_table = 'receivers'
        unique_together = ['email', 'cpf_cnpj']
