# Generated by Django 3.0.5 on 2021-04-23 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fillvalues', '0006_sharechecklist_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharechecklist',
            name='quantity',
        ),
        migrations.AddField(
            model_name='sharewatchlist',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='company',
            name='priceshortsearch',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
