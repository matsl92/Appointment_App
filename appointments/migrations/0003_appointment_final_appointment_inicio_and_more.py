# Generated by Django 4.1.3 on 2023-02-01 01:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='final',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='servicio',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='appointments.servicio'),
        ),
    ]