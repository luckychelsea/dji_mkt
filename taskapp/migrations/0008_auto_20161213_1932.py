# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-13 16:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taskapp', '0007_auto_20161206_2303'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('act_type', models.CharField(choices=[(b'e', '\u0418\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447\u0438'), (b'c', '\u0421\u043e\u0437\u0434\u0430\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447\u0438'), (b'd', '\u0423\u0434\u0430\u043b\u0435\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447\u0438')], max_length=1)),
                ('when', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('-id',), 'permissions': (('can_viewall', '\u0414\u043e\u0441\u0442\u0443\u043f \u043a\u043e \u0432\u0441\u0435\u043c \u0437\u0430\u0434\u0430\u0447\u0430\u043c'),)},
        ),
        migrations.AddField(
            model_name='changelog',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskapp.Task'),
        ),
        migrations.AddField(
            model_name='changelog',
            name='who',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]