# Generated by Django 2.1.3 on 2018-12-03 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('progress', '0009_expansion_aktualny'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expansion',
            options={'ordering': ('-position',), 'verbose_name_plural': 'Expansions'},
        ),
        migrations.AlterModelOptions(
            name='raid',
            options={'ordering': ('-position',), 'verbose_name_plural': 'Raids'},
        ),
    ]
