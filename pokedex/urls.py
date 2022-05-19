from django.urls import re_path as url
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^trainer/$', views.Profile.as_view(), name='profile'),
    url(r'^trainer/(?P<pk>\d+)/$', views.TrainerProfileUpdate.as_view(), name='trainerprofile-update'),
    url(r'^pokemons/$', views.PokemonListView.as_view(), name='pokemons'),
    url(r'^pokemon/(?P<pk>\d+)$', views.PokemonDetailView.as_view(), name='pokemon-detail'),
    url(r'^moves/$', views.MoveListView.as_view(), name='moves'),
    url(r'^move/(?P<pk>\d+)$', views.MoveDetailView.as_view(), name='move-detail'),
    url(r'move/create/$',views.MoveCreate.as_view(), name='move_create'),
    url(r'^move/(?P<pk>\d+)/update/$', views.MoveUpdate.as_view(), name='move-update'),
    url(r'^move/(?P<pk>\d+)/delete/$', views.MoveDelete.as_view(), name='move-delete'),
    url(r'^mypokemons/$', views.PokemonInstanceByTrainerListView.as_view(), name='my-pokemon'),
    url(r'^mypokemon/(?P<pk>[-\w]+)$', views.PokemonInstanceDetailView.as_view(), name='pokemoninstance-detail'),
    url(r'^mypokemon/(?P<pk>[-\w]+)/change/$', views.changePokemonInstanceForm, name='change_pokemon_instance'),
    url(r'^mypokemon/(?P<pk>[-\w]+)/delete/$', views.PokemonInstanceDelete.as_view(), name='pokemoninstance_delete'),
    url(r'^mypokemon/create/$', views.PokemonInstanceCreate.as_view(), name='pokemoninstance_create'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^pokemon/create/$', views.PokemonCreate.as_view(), name='pokemon_create'),
    url(r'^pokemon/(?P<pk>\d+)/update/$', views.PokemonUpdate.as_view(), name='pokemon_update'),
    url(r'^pokemon/(?P<pk>\d+)/delete/$', views.PokemonDelete.as_view(), name='pokemon_delete'),
]
