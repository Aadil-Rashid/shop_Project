# Generated by Django 3.2.4 on 2021-06-22 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(default='', max_length=70, verbose_name='State'),
        ),
    ]
