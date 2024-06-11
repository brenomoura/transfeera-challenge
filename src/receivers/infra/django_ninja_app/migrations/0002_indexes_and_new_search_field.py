from django.db import migrations, models
from django.db.models import Q, F, TextField
from django.db.models.functions import Concat


def populate_search_field(apps, app_schema):
    ReceiverModel = apps.get_model("receivers", "ReceiverModel")
    ReceiverModel.objects.all().annotate(
        search_field_tmp=Concat(
            F("name"),
            F("pix_key_type"),
            F("pix_key"),
            F("status"),
            output_field=models.TextField(),
        )
    ).update(_search_field=F("search_field_tmp"))


class Migration(migrations.Migration):
    dependencies = [
        ("receivers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name='receivermodel',
            name='_search_field',
            field=models.TextField(null=True),
        ),
        migrations.RunPython(
            populate_search_field,
            migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name="receivermodel",
            name="_search_field",
            field=models.TextField(null=False),
        ),
        migrations.AddIndex(
            model_name='receivermodel',
            index=models.Index(fields=['_search_field'], name='receivers__search_bc93ea_idx'),
        ),
    ]
