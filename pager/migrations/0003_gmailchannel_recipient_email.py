# Generated by Django 2.2.4 on 2019-08-24 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pager', '0002_auto_20190824_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='gmailchannel',
            name='recipient_email',
            field=models.EmailField(default='alex@alexsalle.com', max_length=254),
            preserve_default=False,
        ),
    ]
