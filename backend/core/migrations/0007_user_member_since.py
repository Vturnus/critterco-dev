# Generated by Django 3.0.5 on 2020-05-10 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200510_0722'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='member_since',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]