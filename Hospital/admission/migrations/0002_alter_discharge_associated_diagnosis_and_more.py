# Generated by Django 4.2 on 2024-04-05 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discharge',
            name='associated_diagnosis',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='discharge',
            name='final_diagnosis',
            field=models.TextField(blank=True, null=True),
        ),
    ]