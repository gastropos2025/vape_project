from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.text import slugify

class UsuarioPerfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    nombre_marca = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to="usuarios/logos/", blank=True, null=True)
    imagen_principal = models.ImageField(upload_to="usuarios/imagenes/", blank=True, null=True)
    imagen_secundaria = models.ImageField(upload_to="usuarios/imagenes/", blank=True, null=True)
    imagen_notch = models.ImageField(upload_to="usuarios/imagenes/", blank=True, null=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.usuario.username
    
class Sabor(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    sabor1 = models.CharField(max_length=100, blank=True, null=True)
    sabor2 = models.CharField(max_length=100, blank=True, null=True)
    sabor3 = models.CharField(max_length=100, blank=True, null=True)
    efecto = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to="sabores/", blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    informacion = models.TextField()
    sabor = models.ForeignKey(Sabor, on_delete=models.SET_NULL, null=True, related_name="productos")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name="inventario")
    cantidad_disponible = models.PositiveIntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad_disponible} unidades"

class EmailLog(models.Model):
    destinatario = models.EmailField()
    asunto = models.CharField(max_length=255)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(default=now)
    enviado_exitosamente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.asunto} -> {self.destinatario} ({'Enviado' if self.enviado_exitosamente else 'Fallido'})"

# New models for customers and sales
class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    account = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(default=now)
    
    def __str__(self):
        return self.nombre

class Venta(models.Model):
    ESTADO_PEDIDO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('ENVIADO', 'Enviado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]

    METODOS_PAGO = (
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta de Crédito/Débito'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
        ('OTRO', 'Otro'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, related_name="ventas")
    productos = models.ManyToManyField(Producto, through='VentaProducto')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='EFECTIVO')
    fecha_venta = models.DateTimeField(default=now)
    notas = models.TextField(blank=True, null=True)
    estado_pedido = models.CharField(
        max_length=20,
        choices=ESTADO_PEDIDO_CHOICES,
        default='PENDIENTE',
        blank=True,
        null=True
    )
    numero_guia = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Venta {self.id} - {self.cliente.nombre} - {self.fecha_venta.strftime('%Y-%m-%d')}"

class VentaProducto(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Ensure inventory is sufficient before saving
        inventario = self.producto.inventario
        if inventario.cantidad_disponible >= self.cantidad:
            super().save(*args, **kwargs)
            # Update inventory
            inventario.cantidad_disponible -= self.cantidad
            inventario.save()
        else:
            raise ValueError(f"No hay suficiente inventario para {self.producto.nombre}. Disponible: {inventario.cantidad_disponible}")

    def __str__(self):
        return f"{self.venta.id} - {self.producto.nombre} x {self.cantidad}"
    
    def get_subtotal(self):
        return self.cantidad * self.precio_unitario
    