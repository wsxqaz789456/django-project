# Generated by Django 4.1 on 2023-01-06 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_remove_question_ask_comment_question_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_parent',
            field=models.BooleanField(default=False),
        ),
    ]
