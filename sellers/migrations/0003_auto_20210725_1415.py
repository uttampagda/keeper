# Generated by Django 3.1 on 2021-07-25 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0002_remove_seller_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
