# Generated by Django 3.2.2 on 2021-07-07 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bitcoin', '0006_auto_20210707_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='coin_gecho',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.CharField(max_length=200)),
                ('coinsearch', models.CharField(max_length=200)),
            ],
        ),
    ]
