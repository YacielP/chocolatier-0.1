# tienda/admin.py
from django.contrib import admin
from .models import Producto, Categoria

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre', 'descripcion')

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria)