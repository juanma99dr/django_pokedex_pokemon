# Generated by Django 4.0.2 on 2022-04-27 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokedex', '0003_alter_pokemon_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trainerprofile',
            old_name='description',
            new_name='biography',
        ),
    ]
