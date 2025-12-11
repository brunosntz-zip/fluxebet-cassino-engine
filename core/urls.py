from django.contrib import admin
from django.urls import path # <--- Faltou essa linha aqui!
from game import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('acao/<str:tipo>/', views.acao, name='acao'),
    path('apostar/', views.apostar, name='apostar'),
]