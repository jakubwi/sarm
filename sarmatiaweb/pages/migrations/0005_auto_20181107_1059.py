# Generated by Django 2.1.3 on 2018-11-07 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20181107_1057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rekrutacja',
            old_name='rekrutacjaHeal',
            new_name='heal',
        ),
        migrations.RenameField(
            model_name='rekrutacja',
            old_name='rekrutacjaMelee',
            new_name='melee',
        ),
        migrations.RenameField(
            model_name='rekrutacja',
            old_name='rekrutacjaRanged',
            new_name='ranged',
        ),
        migrations.RenameField(
            model_name='rekrutacja',
            old_name='rekrutacjaTank',
            new_name='tank',
        ),
    ]
