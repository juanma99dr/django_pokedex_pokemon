from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pokedex/', include('pokedex.urls')),
    path('', RedirectView.as_view(url='/pokedex/', permanent=True)),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#Habilita el servicio de ficheros estáticos
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]