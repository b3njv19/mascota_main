from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return self.nombre


