# Generated by Django 5.1.1 on 2025-02-06 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_generator', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email_token',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
