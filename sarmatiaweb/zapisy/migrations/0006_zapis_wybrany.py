# Generated by Django 2.1.3 on 2018-12-10 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zapisy', '0005_auto_20181210_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='zapis',
            name='wybrany',
            field=models.BooleanField(default=False),
        ),
    ]
