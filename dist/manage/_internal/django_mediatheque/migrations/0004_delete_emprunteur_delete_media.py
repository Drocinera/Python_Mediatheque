# Generated by Django 5.0.7 on 2024-08-08 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_mediatheque', '0003_delete_jeudeplateau_media_artiste_media_createur_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Emprunteur',
        ),
        migrations.DeleteModel(
            name='Media',
        ),
    ]
