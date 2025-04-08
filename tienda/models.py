from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)  # Ej: "Combos", "Simples"
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)  # Ej: "Chocolate con almendras"
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Ej: 5.99
    imagen = models.ImageField(upload_to='productos/')  # Las imágenes se guardan en /media/productos/
    disponible = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre