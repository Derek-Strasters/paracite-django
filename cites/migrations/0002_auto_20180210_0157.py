# Generated by Django 2.0.2 on 2018-02-10 01:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cites', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paragraph',
            name='level',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paragraph',
            name='parent_paragraph',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cites.Paragraph'),
        ),
    ]
