from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('productos/', views.explorar_productos, name='productos'),
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('obtener-carrito/', views.obtener_carrito, name='obtener_carrito'),
    path('finalizar-pedido/', views.finalizar_pedido, name='finalizar_pedido'),
]