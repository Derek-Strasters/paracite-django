# Generated by Django 2.0.2 on 2018-02-21 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cites', '0003_auto_20180211_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paragraph',
            name='level',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='story',
            name='rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='story',
            name='score',
            field=models.BigIntegerField(default=0),
        ),
    ]
