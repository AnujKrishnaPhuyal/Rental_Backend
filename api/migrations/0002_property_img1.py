# Generated by Django 5.0.4 on 2024-05-09 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='img1',
            field=models.ImageField(default='', upload_to='item_images/'),
            preserve_default=False,
        ),
    ]
