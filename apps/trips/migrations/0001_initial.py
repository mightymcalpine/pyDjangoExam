# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-04 19:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('logReg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripsDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=128)),
                ('plan', models.TextField()),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updateAt', models.DateTimeField(auto_now=True)),
                ('plannedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tripsPlanned', to='logReg.UserDB')),
                ('usersJoined', models.ManyToManyField(related_name='tripsJoined', to='logReg.UserDB')),
            ],
        ),
    ]
