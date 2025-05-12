from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.shortcuts import render
from .models import Sabor, UsuarioPerfil, Inventario, Producto, Cliente, Venta, VentaProducto
from django.http import JsonResponse
from .forms import SaborForm, ProductoForm, InventarioForm, ClienteForm, VentaForm, VentaProductoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def index(request):
    # Obtener todos los sabores
    sabores = Sabor.objects.all()
    perfil = None
    
    # Si el usuario está autenticado, intentar obtener su perfil
    if request.user.is_authenticated:
        try:
            perfil = request.user.perfil  # Acceder al perfil relacionado mediante el related_name 'perfil'
        except UsuarioPerfil.DoesNotExist:
            perfil = None  # Manejar el caso en que el perfil no exista
    
    # Renderizar la plantilla con el contexto
    return render(request, 'index.html', {
        'sabores': sabores,
        'perfil': perfil
    })

def get_productos_por_sabor(request, sabor_id):
    try:
        sabor = Sabor.objects.get(id=sabor_id)
        productos = Producto.objects.filter(sabor=sabor)
        data = {
            'sabor': {
                'nombre': sabor.nombre,
                'sabor1': sabor.sabor1,
                'sabor2': sabor.sabor2,
                'sabor3': sabor.sabor3,
                'efecto': sabor.efecto,
            },
            'productos': [
                {
                    'nombre': producto.nombre,
                    'informacion': producto.informacion,
                    'precio': producto.precio,
                    'imagen': producto.imagen.url if producto.imagen else None,
                } for producto in productos
            ]
        }
        return JsonResponse(data)
    except Sabor.DoesNotExist:
        return JsonResponse({'error': 'Sabor no encontrado'}, status=404)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        # Send email (replace with your email settings)
        send_mail(
            "Prueba de Correo",
            "Este es un correo de prueba desde Django.",
            "santiago.perez@outlook.com",
            ["destinatario@hotmail.com"],
            fail_silently=False,
        )
        return render(request, 'index.html')
    return render(request, 'index.html') # Adjust template name

# Flavor Management Views
@login_required
def sabor_list(request):
    sabores = Sabor.objects.all()
    return render(request, 'sabores/sabor_list.html', {'sabores': sabores})

@login_required
def sabor_create(request):
    if request.method == 'POST':
        form = SaborForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sabor creado exitosamente.')
            return redirect('sabor_list')
    else:
        form = SaborForm()
    return render(request, 'sabores/sabor_form.html', {'form': form, 'action': 'Crear'})

@login_required
def sabor_edit(request, pk):
    sabor = get_object_or_404(Sabor, pk=pk)
    if request.method == 'POST':
        form = SaborForm(request.POST, request.FILES, instance=sabor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sabor actualizado exitosamente.')
            return redirect('sabor_list')
    else:
        form = SaborForm(instance=sabor)
    return render(request, 'sabores/sabor_form.html', {'form': form, 'action': 'Editar'})

@login_required
def sabor_delete(request, pk):
    sabor = get_object_or_404(Sabor, pk=pk)
    if request.method == 'POST':
        sabor.delete()
        messages.success(request, 'Sabor eliminado exitosamente.')
        return redirect('sabor_list')
    return render(request, 'sabores/sabor_confirm_delete.html', {'sabor': sabor})

# Product Management Views
@login_required
def producto_list(request):
    productos = Producto.objects.all()
    return render(request, 'sabores/producto_list.html', {'productos': productos})

@login_required
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('producto_list')
    else:
        form = ProductoForm()
    return render(request, 'sabores/producto_form.html', {'form': form, 'action': 'Crear'})

@login_required
def producto_edit(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('producto_list')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'sabores/producto_form.html', {'form': form, 'action': 'Editar'})

@login_required
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('producto_list')
    return render(request, 'sabores/producto_confirm_delete.html', {'producto': producto})

@login_required
def inventario_list(request):
    inventarios = Inventario.objects.all()
    return render(request, 'sabores/inventario_list.html', {'inventarios': inventarios})

@login_required
def inventario_create(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro de inventario creado exitosamente.')
            return redirect('inventario_list')
    else:
        form = InventarioForm()
    return render(request, 'sabores/inventario_form.html', {'form': form, 'action': 'Crear'})

@login_required
def inventario_edit(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        form = InventarioForm(request.POST, instance=inventario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro de inventario actualizado exitosamente.')
            return redirect('inventario_list')
    else:
        form = InventarioForm(instance=inventario)
    return render(request, 'sabores/inventario_form.html', {'form': form, 'action': 'Editar'})

@login_required
def inventario_delete(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        inventario.delete()
        messages.success(request, 'Registro de inventario eliminado exitosamente.')
        return redirect('inventario_list')
    return render(request, 'sabores/inventario_confirm_delete.html', {'inventario': inventario})

# AJAX View for Products Modal
def get_productos_by_sabor(request, sabor_id):
    sabor = get_object_or_404(Sabor, id=sabor_id)
    productos = Producto.objects.filter(sabor=sabor)
    data = [
        {
            'id': producto.id,
            'nombre': producto.nombre,
            'informacion': producto.informacion,
            'precio': str(producto.precio),
            'imagen': producto.imagen.url if producto.imagen else ''
        }
        for producto in productos
    ]
    return JsonResponse({'productos': data})

# New views for Cliente and Venta
@login_required
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'ventas/cliente_list.html', {'clientes': clientes})

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'ventas/cliente_form.html', {'form': form})

@login_required
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'ventas/cliente_form.html', {'form': form})

@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente.')
        return redirect('cliente_list')
    return render(request, 'ventas/cliente_confirm_delete.html', {'cliente': cliente})

@login_required
def venta_list(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas/venta_list.html', {'ventas': ventas})

@login_required
def venta_create(request):
    VentaProductoFormSet = modelformset_factory(VentaProducto, form=VentaProductoForm, extra=1, can_delete=True)
    if request.method == 'POST':
        form = VentaForm(request.POST)
        formset = VentaProductoFormSet(request.POST, queryset=VentaProducto.objects.none())
        if form.is_valid() and formset.is_valid():
            venta = form.save()
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    venta_producto = form.save(commit=False)
                    venta_producto.venta = venta
                    venta_producto.save()
            messages.success(request, 'Venta registrada exitosamente.')
            return redirect('venta_list')
    else:
        form = VentaForm()
        formset = VentaProductoFormSet(queryset=VentaProducto.objects.none())
    return render(request, 'ventas/venta_form.html', {'form': form, 'formset': formset})

@login_required
def venta_edit(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    VentaProductoFormSet = modelformset_factory(VentaProducto, form=VentaProductoForm, extra=1, can_delete=True)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        formset = VentaProductoFormSet(request.POST, queryset=VentaProducto.objects.filter(venta=venta))
        if form.is_valid() and formset.is_valid():
            # Revert inventory for existing VentaProducto before saving changes
            for vp in VentaProducto.objects.filter(venta=venta):
                inventario = vp.producto.inventario
                inventario.cantidad_disponible += vp.cantidad
                inventario.save()
            form.save()
            for form in formset:
                if form.cleaned_data:
                    if form.cleaned_data.get('DELETE', False):
                        if form.instance.pk:
                            form.instance.delete()
                    else:
                        venta_producto = form.save(commit=False)
                        venta_producto.venta = venta
                        venta_producto.save()
            messages.success(request, 'Venta actualizada exitosamente.')
            return redirect('venta_list')
    else:
        form = VentaForm(instance=venta)
        formset = VentaProductoFormSet(queryset=VentaProducto.objects.filter(venta=venta))
    return render(request, 'ventas/venta_form.html', {'form': form, 'formset': formset})

@login_required
def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        # Revert inventory for all VentaProducto items
        for vp in VentaProducto.objects.filter(venta=venta):
            inventario = vp.producto.inventario
            inventario.cantidad_disponible += vp.cantidad
            inventario.save()
        venta.delete()
        messages.success(request, 'Venta eliminada exitosamente.')
        return redirect('venta_list')
    return render(request, 'ventas/venta_confirm_delete.html', {'venta': venta})

@login_required
def venta_detail(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    venta_productos = VentaProducto.objects.filter(venta=venta)
    return render(request, 'ventas/venta_detail.html', {'venta': venta, 'venta_productos': venta_productos})
