# Generated by Django 2.1.3 on 2018-11-09 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rejestracja', '0004_podaniekomentarze'),
    ]

    operations = [
        migrations.RenameField(
            model_name='podaniekomentarze',
            old_name='user',
            new_name='author',
        ),
    ]
