# Generated by Django 4.0.10 on 2024-11-25 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
    ]
