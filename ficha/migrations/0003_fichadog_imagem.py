# Generated by Django 4.2.4 on 2023-09-09 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ficha', '0002_remove_vacina_data_reforco_vacina_nova_dose_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fichadog',
            name='imagem',
            field=models.ImageField(default=0, upload_to='static/img/'),
            preserve_default=False,
        ),
    ]
