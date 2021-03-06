# Generated by Django 2.1.5 on 2021-09-21 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20210916_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='petition',
            name='answer',
            field=models.TextField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='petition',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='petition_doctor', to='core.Doctor'),
        ),
        migrations.AlterField(
            model_name='petition',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='petition_patient', to='core.Patient'),
        ),
    ]
