# Generated by Django 3.1.6 on 2021-04-16 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='PLAYER_1_WINS',
            field=models.BooleanField(default=False),
        ),
    ]