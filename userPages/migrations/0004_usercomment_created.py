# Generated by Django 3.1.3 on 2021-04-22 08:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userPages', '0003_usercomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercomment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
