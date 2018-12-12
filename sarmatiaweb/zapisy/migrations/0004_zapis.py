# Generated by Django 2.1.3 on 2018-12-10 10:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userpostac_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zapisy', '0003_auto_20181207_1252'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zapis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gotowosc', models.CharField(choices=[('3', 'Zależy mi na raidzie'), ('2', 'Mogę iść, mogę nie iść'), ('1', 'Pójdę wyłącznie jeśli będę potrzebny')], default=3, max_length=2)),
                ('komentarz', models.CharField(max_length=120)),
                ('kiedy', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('czym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserPostac')),
                ('kto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('na_co', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zapisy.Event')),
            ],
            options={
                'verbose_name_plural': 'Zapisy',
            },
        ),
    ]
