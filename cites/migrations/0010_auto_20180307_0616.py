# Generated by Django 2.0.2 on 2018-03-07 06:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cites', '0009_paragraph_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paragraph',
            options={'ordering': ['-score', 'created_date']},
        ),
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ['-score', 'created_date']},
        ),
        migrations.AlterField(
            model_name='paragraph',
            name='url',
            field=models.URLField(max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='votingrecord',
            name='paragraph',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cites.Paragraph'),
        ),
        migrations.AlterField(
            model_name='votingrecord',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='paracite_profile.Profile'),
        ),
    ]
