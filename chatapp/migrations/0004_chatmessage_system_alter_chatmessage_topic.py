# Generated by Django 5.1.1 on 2024-10-09 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0003_chatmessage_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='system',
            field=models.CharField(default='default_system', max_length=100),
        ),
        migrations.AlterField(
            model_name='chatmessage',
            name='topic',
            field=models.CharField(default='default_topic', max_length=100),
        ),
    ]