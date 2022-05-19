from django.db import models
from django.urls import reverse
import uuid
from datetime import datetime
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.html import escape
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
# models


class Gender(models.Model):
    name = models.CharField(
        max_length=20, help_text="Ingrese el nombre del genero.")

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(
        max_length=20, help_text="Ingrese el tipo a añadir.")

    def __str__(self):
        return self.name


class Generation(models.Model):
    name = models.CharField(
        max_length=20, help_text="Ingrese la generacion correspondiente al pokemon.")

    def __str__(self):
        return self.name


class Pokemon(models.Model):
    numPokedex = models.PositiveIntegerField(
        primary_key=True, verbose_name="Nº Pokedex", help_text="Numero correspondiente a la entrada en la pokedex del pokemon en cuestion.")

    name = models.CharField(max_length=50, help_text="Nombre del pokemon")

    description = models.TextField(
        max_length=255, help_text="Descripcion del pokemon.")

    image = models.ImageField(
        help_text="Imagen del pokemon", default='default.jpg')

    type = models.ManyToManyField(
        Type, help_text="Seleccione su(s) tipo(s) correspondiente(s).")

    generation = models.ForeignKey("Generation", on_delete=models.SET_NULL, null=True,
                                   help_text="Generacion en la que fue incluida el pokemon.")
    evolutions = models.ManyToManyField(
        "Pokemon", help_text="Selecciona su linea evolutiva", blank=True)

    stats = models.PositiveIntegerField(
        default='50', help_text='Estado del pokemon',
        validators=[
                MaxValueValidator(100),
                MinValueValidator(1)
        ]
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pokemon-detail', args=[str(self.numPokedex)])

    def get_absolute_urlPrev(self):
        if (self.numPokedex > 1):
            return reverse('pokemon-detail', args=[str(self.numPokedex-1)])
        else:
            return reverse('pokemon-detail', args=[str(self.numPokedex)])

    def get_absolute_urlNext(self):
        if (self.numPokedex > 0):
            return reverse('pokemon-detail', args=[str(self.numPokedex+1)])

    def display_type(self):
        return ', '.join([type.name for type in self.type.all()[:2]])
    display_type.short_description = 'Types'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def image_tagView(self):
        return mark_safe('<img src="%s" />' % (self.image.url))

    def image_tagView50(self):
        return mark_safe('<img src="%s" width="200" height="200<" />' % (self.image.url))

    image_tag.short_description = 'Image'
# TODO: limitar a maximo dos elecciones el campo type del modelo Pokemon


class PokemonInstance(models.Model):
    identifier = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text="Id único para este ejemplar")

    pokemon = models.ForeignKey(
        "Pokemon", on_delete=models.SET_NULL, null=True)

    nickname = models.CharField(
        max_length=50, help_text="Mote para el pokémon", default=pokemon.name)

    level = models.PositiveIntegerField(help_text="El nivel debe estar entre 1 y 100 incluidos.", default=1,
                                        validators=[MaxValueValidator(100), MinValueValidator(1)])

    date_of_birth = models.DateField(default=datetime.now)

    trainer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    gender = models.ForeignKey("Gender", on_delete=models.SET_NULL, null=True,
                               help_text="Género del pokemon.")

    moves = models.ManyToManyField(
        "Move", help_text="Selecciona sus movimientos")

    def display_moves(self):
        return ', '.join([move.name for move in self.moves.all()[:4]])
    display_moves.short_description = 'Moves'

    class Meta:
        ordering = ["level"]

    def get_absolute_url(self):
        return reverse('pokemoninstance-detail', args=[str(self.identifier)])


class Move(models.Model):
    name = models.CharField(max_length=50, help_text="Nombre del ataque")
    type = models.ForeignKey(
        "Type", on_delete=models.SET_NULL, null=True, help_text="Tipo del movimiento")
    cATEGORY_LIST = (
        ('P', 'Physical'),
        ('E', 'Special'),
        ('S', 'Status'),
    )
    category = models.CharField(
        max_length=1, choices=cATEGORY_LIST, default='P', help_text='categoria del movimiento')

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('move-detail', args=[str(self.id)])


class TrainerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePic = models.ImageField(default="default.jpg")
    biography = models.TextField(
        max_length=255, help_text="Descripcion del usuario.")

    def get_absolute_url(self):
        return reverse('profile',)

    def profilePic_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.profilePic.url))
    profilePic_tag.short_description = 'Profile Picture'
    # TODO: Falta añadir un atributo para el numero de pokemon capturados
    
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            TrainerProfile.objects.create(user=instance)
        instance.trainerprofile.save()

    class Meta:
        ...
        permissions = (("is_admin", "Admin"),)
