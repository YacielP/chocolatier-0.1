from django.shortcuts import render
from .models import Producto, Categoria  # Importamos los modelos
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def obtener_carrito(request):
    try:
        carrito = request.session.get('carrito', {})
        total_items = sum(carrito.values()) if carrito else 0
        
        return JsonResponse({
            'success': True,
            'total_items': total_items
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

# Vista para la página de inicio
def inicio(request):
    return render(request, 'inicio.html')

# Vista para "Sobre Nosotros"
def sobre_nosotros(request):
    return render(request, 'sobre_nosotros.html')

# Vista para mostrar productos
def explorar_productos(request):
    # Obtenemos la categoría seleccionada (o 'todos' por defecto)
    categoria_seleccionada = request.GET.get('categoria', 'todos')
    
    # Filtramos productos disponibles
    productos = Producto.objects.filter(disponible=True)
    
    # Si no es 'todos', filtramos por categoría
    if categoria_seleccionada != 'todos':
        productos = productos.filter(categoria__nombre=categoria_seleccionada)
    
    # Obtenemos todas las categorías para los botones de filtro
    categorias = Categoria.objects.all()
    
    return render(request, 'productos.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
    })

from django.shortcuts import render, redirect
from django.http import JsonResponse

def agregar_al_carrito(request):
    if request.method == 'POST':
        try:
            producto_id = int(request.POST.get('producto_id'))
            cantidad = int(request.POST.get('cantidad', 1))
            
            carrito = request.session.get('carrito', {})
            producto_id_str = str(producto_id)
            
            if producto_id_str in carrito:
                carrito[producto_id_str] += cantidad
            else:
                carrito[producto_id_str] = cantidad
                
            request.session['carrito'] = carrito
            
            # Respuesta JSON más detallada
            return JsonResponse({
                'success': True,
                'message': 'Producto añadido al carrito',
                'carrito_count': sum(carrito.values()),
                'producto_id': producto_id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    }, status=405)

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0
    
    for producto_id, cantidad in carrito.items():
        try:
            # Convertir a entero por si acaso
            producto_id_int = int(producto_id)
            producto = Producto.objects.get(id=producto_id_int)
            subtotal = producto.precio * cantidad
            total += subtotal
            productos.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
        except (ValueError, Producto.DoesNotExist):
            # Si el ID no es válido o el producto no existe, lo eliminamos del carrito
            del request.session['carrito'][producto_id]
            request.session.modified = True
    
    return render(request, 'carrito.html', {
        'productos': productos,
        'total': total
    })

def finalizar_pedido(request):
    if not request.session.get('carrito'):
        return redirect('ver_carrito')

    carrito = request.session.get('carrito', {})
    
    if not carrito:
        return redirect('ver_carrito')
    
    if request.method == 'POST':
        
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        requiere_domicilio = request.POST.get('domicilio') == 'on'
        direccion = request.POST.get('direccion', '')
        
        # Generar mensaje para WhatsApp
        mensaje = f"¡Hola! Quiero hacer un pedido:\n\n"
        
        total = 0
        for producto_id, cantidad in carrito.items():
            producto = Producto.objects.get(id=producto_id)
            subtotal = producto.precio * cantidad
            total += subtotal
            mensaje += f"- {producto.nombre} x{cantidad}: ${subtotal}\n"
        
        mensaje += f"\nTotal: ${total}\n"
        mensaje += f"Cliente: {nombre}\n"
        mensaje += f"Teléfono: {telefono}\n"
        
        if requiere_domicilio:
            mensaje += f"Dirección: {direccion}\n"
        else:
            mensaje += "Recogeré en tienda.\n"
        
        # Limpiar carrito
        request.session['carrito'] = {}
        
        # Redirigir a WhatsApp
        whatsapp_url = f"https://wa.me/5355333152?text={mensaje.replace(' ', '%20').replace('\n', '%0A')}"
        return redirect(whatsapp_url)
    
    return render(request, 'finalizar_pedido.html')