from django.shortcuts import render
from django.views import generic
from .models import Pokemon, PokemonInstance, Gender, Generation, Type, TrainerProfile, Move
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from next_prev import next_in_order, prev_in_order
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .forms import PokemonInstanceForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from .forms import SignUpForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def index(request):

    num_users = TrainerProfile.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(
        request,
        "index.html",
        context={"num_users": num_users, }
    )


class Profile(LoginRequiredMixin, generic.ListView):
    model = TrainerProfile
    context_object_name = "profile"
    template_name = "profile.html"

    def get_queryset(self):
        return TrainerProfile.objects.filter(user=self.request.user)


class PokemonListView(generic.ListView):
    model = Pokemon
    context_object_name = "pokemon_list"
    template_name = "pokemons/pokemon_list.html"

    def get_queryset(self):
        return Pokemon.objects.order_by('numPokedex')


class PokemonDetailView(generic.DetailView):
    model = Pokemon
    context_object_name = "pokemon"

class MoveDetailView(generic.DetailView):
    model = Move
    context_object_name = "move"

class MoveListView(generic.ListView):
    model = Move
    context_object_name = "move_list"
    template_name = "moves/move_list.html"

    def get_queryset(self):
        return Move.objects.order_by('name')


class PokemonInstanceByTrainerListView(LoginRequiredMixin, generic.ListView):
    model = PokemonInstance
    template_name = "pokedex/pokemonInstanceByTrainerList.html"

    def get_queryset(self):
        return PokemonInstance.objects.filter(trainer=self.request.user)


class PokemonInstanceDetailView(LoginRequiredMixin, generic.DetailView):
    model = PokemonInstance


def changePokemonInstanceForm(request, pk):

    pokemonInstance = get_object_or_404(PokemonInstance, pk = pk)
    if request.method == 'POST':
        form = PokemonInstanceForm(request.POST)
        if form.is_valid():
            pokemonInstance.nickname = form.cleaned_data["nickname"]
            pokemonInstance.level = form.cleaned_data["level"]
            pokemonInstance.date_of_birth = form.cleaned_data["date_of_birth"]
            pokemonInstance.trainer = form.cleaned_data["trainer"]
            pokemonInstance.gender = form.cleaned_data["gender"]
            pokemonInstance.moves.set(form.cleaned_data["moves"])
            pokemonInstance.save()
            return HttpResponseRedirect(reverse('my-pokemon'))

    else:
        form = PokemonInstanceForm(initial={"nickname":pokemonInstance.nickname, "level":pokemonInstance.level, "date_of_birth":pokemonInstance.date_of_birth, "trainer":pokemonInstance.trainer, "gender":pokemonInstance.gender})

    return render(request, 'pokedex/changePokemonInstance.html', {'form': form, 'PokemonInstance': pokemonInstance})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# CRUD for Pokemon
class PokemonCreate(CreateView):
    model = Pokemon
    fields = "__all__"

class PokemonUpdate(UpdateView):
    model = Pokemon
    fields = "__all__"

class PokemonDelete(DeleteView):
    model = Pokemon
    success_url = reverse_lazy('pokemon-list')
    
    
# CRUD for PokemonInstance
class PokemonInstanceCreate(CreateView):
    model = PokemonInstance
    fields = "__all__"

class PokemonInstanceDelete(DeleteView):
    model = PokemonInstance
    success_url = reverse_lazy('my-pokemon')
    

# CRUD for Move
class MoveCreate(CreateView):
    model = Move
    fields = "__all__"
    
class MoveUpdate(UpdateView):
    model = Move
    fields = "__all__"
    
class MoveDelete(DeleteView):
    model = Move
    success_url = reverse_lazy('moves')
    
    
#CRUD for TrainerProfile
class TrainerProfileUpdate(UpdateView):
    model = TrainerProfile
    fields = ["profilePic", "biography",]