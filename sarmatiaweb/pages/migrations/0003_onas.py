# Generated by Django 2.1.3 on 2018-12-17 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_killshot'),
    ]

    operations = [
        migrations.CreateModel(
            name='Onas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1024)),
            ],
            options={
                'verbose_name_plural': 'O nas',
            },
        ),
    ]