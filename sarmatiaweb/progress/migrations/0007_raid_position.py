# Generated by Django 2.1.3 on 2018-11-22 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0006_auto_20181122_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='raid',
            name='position',
            field=models.PositiveIntegerField(blank=True, help_text='Wpisz cyfrę odpowiadającą kolejności progressu', null=True),
        ),
    ]
