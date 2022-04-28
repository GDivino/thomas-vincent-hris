# Generated by Django 4.0.2 on 2022-04-28 03:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hris', '0008_alter_assignmentt_base_pay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentt',
            name='aproject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hris.projectt'),
        ),
        migrations.AlterField(
            model_name='assignmentt',
            name='aworker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hris.workert'),
        ),
    ]
