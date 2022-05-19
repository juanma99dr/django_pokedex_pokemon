from django.contrib import admin
from .models import Pokemon, PokemonInstance, Gender, Generation, Type, Move, TrainerProfile, User
from next_prev import next_in_order, prev_in_order
admin.site.register(Gender)
admin.site.register(Generation)
admin.site.register(Type)

#backend views
@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ("numPokedex", "name","image_tag","display_type")
    ordering = ("numPokedex","name")
    list_filter = ("generation","type")
    fields = ("numPokedex","name","description",("image","image_tag"),"type","stats","generation","evolutions",)
    readonly_fields = ['image_tag']


@admin.register(PokemonInstance)
class PokemonInstanceAdmin(admin.ModelAdmin):
    list_display = ("nickname","pokemon","display_moves","trainer")
    list_filter = ("trainer","pokemon")
    ordering =("trainer","pokemon")

@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = ("user","profilePic_tag")
    fields = ("user",("profilePic","profilePic_tag"),"biography")
    readonly_fields = ['profilePic_tag']
    
@admin.register(Move)
class PokemonInstanceAdmin(admin.ModelAdmin):
    list_display = ("name","type","category",)
    list_filter = ("category","type")
