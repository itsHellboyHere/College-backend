# Generated by Django 4.0.10 on 2024-11-25 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0004_remove_subject_faculty'),
        ('faculties', '0003_faculty_subject_alter_faculty_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='faculties', to='subjects.subject'),
        ),
    ]
