# Generated by Django 2.1.3 on 2018-11-12 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_auto_20181109_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='klasa',
            name='name',
            field=models.CharField(blank=True, default='', help_text="Tworząc nową klasę, zaznacz role w polu 'rekrutacja'.", max_length=50, null=True, unique=True),
        ),
    ]
