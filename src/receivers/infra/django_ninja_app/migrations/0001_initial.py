# Generated by Django 5.0.6 on 2024-06-10 01:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ReceiverModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.TextField()),
                ("email", models.EmailField(max_length=250, null=True, unique=True)),
                ("cpf_cnpj", models.CharField(max_length=20, unique=True)),
                (
                    "pix_key_type",
                    models.CharField(
                        choices=[
                            ("CPF", "CPF"),
                            ("CNPJ", "CNPJ"),
                            ("EMAIL", "EMAIL"),
                            ("TELEFONE", "TELEFONE"),
                            ("CHAVE_ALEATORIA", "CHAVE_ALEATORIA"),
                        ],
                        max_length=100,
                    ),
                ),
                ("pix_key", models.CharField(max_length=140)),
                (
                    "status",
                    models.CharField(
                        choices=[("VALIDATED", "VALIDATED"), ("DRAFT", "DRAFT")],
                        default="DRAFT",
                        max_length=15,
                    ),
                ),
                ("bank_code", models.IntegerField(null=True)),
                ("agency_code", models.CharField(max_length=11, null=True)),
                ("account_type", models.CharField(max_length=100, null=True)),
                ("account_code", models.CharField(max_length=12, null=True)),
            ],
            options={
                "db_table": "receivers",
                "unique_together": {("email", "cpf_cnpj")},
            },
        ),
    ]
