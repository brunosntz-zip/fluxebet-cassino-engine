from django.contrib import admin
from django.urls import path
from game import views  # Importando suas views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),             # Home do site
    path('acao/<str:tipo>/', views.acao, name='acao'), # Link para Hit/Stand
]