# Generated by Django 4.1 on 2023-01-13 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_question_is_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='is_parent',
            field=models.BooleanField(default=True),
        ),
    ]
