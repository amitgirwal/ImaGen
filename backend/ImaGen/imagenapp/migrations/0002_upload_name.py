# Generated by Django 4.1.5 on 2023-01-18 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagenapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
