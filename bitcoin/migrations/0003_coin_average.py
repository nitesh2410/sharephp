# Generated by Django 3.0.5 on 2021-04-28 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bitcoin', '0002_auto_20210423_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='coin_average',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.CharField(max_length=200)),
                ('volume', models.FloatField()),
                ('average', models.FloatField()),
            ],
        ),
    ]
