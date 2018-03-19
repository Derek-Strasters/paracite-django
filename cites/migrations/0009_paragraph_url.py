from django.db import migrations, models

from cites.converters import id_to_url


def gen_url(apps, schema_editor):
    Paragraph = apps.get_model('cites', 'Paragraph')
    for row in Paragraph.objects.all():
        row.url = id_to_url(row.id)
        row.save()


class Migration(migrations.Migration):
    dependencies = [
        ('cites', '0008_auto_20180227_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='paragraph',
            name='url',
            field=models.CharField(default='ERROR', max_length=8),
            preserve_default=False,
        ),
        migrations.RunPython(gen_url),
    ]
