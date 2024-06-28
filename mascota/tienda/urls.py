from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cargar_producto/', views.cargar_producto, name='cargar_producto'),
    path('pago/crear/', views.crear_pago, name='crear_pago'),
    path('pago/completado/', views.pago_completado, name='pago_completado'),
    path('pago/cancelado/', views.pago_cancelado, name='pago_cancelado'),
]
