# Generated by Django 4.0.2 on 2022-04-20 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hris', '0005_alter_workert_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workert',
            name='image',
            field=models.ImageField(blank=True, upload_to='worker'),
        ),
    ]
