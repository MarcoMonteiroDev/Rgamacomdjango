# Generated by Django 5.1.7 on 2025-03-31 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_promo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promo',
            old_name='imagem',
            new_name='imagem_promo',
        ),
    ]
