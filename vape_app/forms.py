from django import forms
from .models import Cliente, Venta, VentaProducto, Sabor, Producto, Inventario

class SaborForm(forms.ModelForm):
    class Meta:
        model = Sabor
        fields = ['nombre', 'sabor1', 'sabor2', 'sabor3', 'efecto', 'imagen']
        widgets = {
            'efecto': forms.Textarea(attrs={'rows': 4}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'informacion', 'sabor', 'precio', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'informacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'sabor': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['producto', 'cantidad_disponible']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad_disponible': forms.NumberInput(attrs={'min': 0}),
        }

    def clean_producto(self):
        producto = self.cleaned_data['producto']
        # Check if the product already has an inventory record (except for the instance being edited)
        if self.instance.pk:
            if Inventario.objects.filter(producto=producto).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Este producto ya tiene un registro de inventario.")
        else:
            if Inventario.objects.filter(producto=producto).exists():
                raise forms.ValidationError("Este producto ya tiene un registro de inventario.")
        return producto
    
# New forms for Cliente and Venta
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'direccion','account']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'account': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'metodo_pago', 'total', 'notas', 'estado_pedido', 'numero_guia']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estado_pedido': forms.Select(attrs={'class': 'form-control'}),
            'numero_guia': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VentaProductoForm(forms.ModelForm):
    class Meta:
        model = VentaProducto
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
        }