# Generated by Django 4.1 on 2023-01-06 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_question_ask_comment_delete_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='ask_comment',
        ),
        migrations.AddField(
            model_name='question',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='sales.question'),
        ),
    ]
