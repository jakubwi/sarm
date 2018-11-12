# Generated by Django 2.1.3 on 2018-11-12 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rejestracja', '0007_auto_20181112_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podanie',
            name='klasa',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='pages.Klasa'),
        ),
        migrations.AlterField(
            model_name='podanie',
            name='mainspec',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='mainspec', to='rejestracja.Rola'),
        ),
        migrations.AlterField(
            model_name='podanie',
            name='offspec',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='offspec', to='rejestracja.Rola'),
        ),
        migrations.AlterField(
            model_name='podanie',
            name='plec',
            field=models.CharField(blank=True, choices=[('K', 'K'), ('M', 'M')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='podanie',
            name='rasa',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='rejestracja.Rasa'),
        ),
        migrations.AlterField(
            model_name='podanie',
            name='serwer',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='rejestracja.Serwer'),
        ),
        migrations.AlterField(
            model_name='rasa',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rola',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='serwer',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
