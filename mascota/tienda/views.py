from django.shortcuts import render, redirect
from .forms import ProductoForm
from .models import Producto
from paypalrestsdk import Payment
import paypalrestsdk
from django.conf import settings

# Configuración de PayPal
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # 'sandbox' o 'live'
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

def home(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/tienda.html', {'productos': productos})

def cargar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductoForm()
    return render(request, 'tienda/cargar_producto.html', {'form': form})

def crear_pago(request):
    print("Crear pago iniciado")  # Debug
    pago = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri('/pago/completado/'),
            "cancel_url": request.build_absolute_uri('/pago/cancelado/')
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Nombre del Producto",
                    "sku": "001",
                    "price": "10.00",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "10.00",
                "currency": "USD"
            },
            "description": "Descripción de la compra."
        }]
    })

    if pago.create():
        print("Pago creado con éxito")  # Debug
        for link in pago.links:
            if link.method == "REDIRECT":
                print(f"Redireccionando a {link.href}")  # Debug
                return redirect(link.href)
    else:
        print(f"Error al crear el pago: {pago.error}")  # Debug
        return render(request, 'pago_error.html', {'error': pago.error})

def pago_completado(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    pago = Payment.find(payment_id)
    if pago.execute({"payer_id": payer_id}):
        return render(request, 'pago_exito.html')
    else:
        return render(request, 'pago_error.html', {'error': pago.error})

def pago_cancelado(request):
    return render(request, 'pago_cancelado.html')
