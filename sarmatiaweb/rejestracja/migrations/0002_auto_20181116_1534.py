# Generated by Django 2.1.3 on 2018-11-16 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rejestracja', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='podanie',
            options={'ordering': ('-date',), 'verbose_name_plural': 'Podania'},
        ),
    ]
