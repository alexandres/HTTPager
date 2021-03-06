# Generated by Django 2.2.4 on 2019-08-24 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import pager.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='GmailChannel',
            fields=[
                ('channel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pager.Channel')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
            ],
            bases=('pager.channel',),
        ),
        migrations.CreateModel(
            name='SlackChannel',
            fields=[
                ('channel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pager.Channel')),
                ('webhook_url', models.CharField(max_length=255)),
                ('channel', models.CharField(max_length=255)),
            ],
            bases=('pager.channel',),
        ),
        migrations.CreateModel(
            name='TelegramChannel',
            fields=[
                ('channel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pager.Channel')),
                ('token', models.CharField(max_length=255)),
                ('chat_id', models.IntegerField()),
            ],
            bases=('pager.channel',),
        ),
        migrations.CreateModel(
            name='Pager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('secret', models.CharField(default=pager.models.gen_secret, max_length=255, unique=True)),
                ('slug', models.CharField(max_length=255, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='channel',
            name='pagers',
            field=models.ManyToManyField(to='pager.Pager'),
        ),
        migrations.AddField(
            model_name='channel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
