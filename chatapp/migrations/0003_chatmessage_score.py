# Generated by Django 5.1.1 on 2024-10-08 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0002_remove_chatmessage_created_at_chatmessage_timestamp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]