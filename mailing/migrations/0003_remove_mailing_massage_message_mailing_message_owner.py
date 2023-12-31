# Generated by Django 4.2.3 on 2023-12-30 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailing', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailing',
            name='massage',
        ),
        migrations.AddField(
            model_name='message',
            name='mailing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing'),
        ),
        migrations.AddField(
            model_name='message',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
