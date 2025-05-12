from django.contrib import admin
from .models import Producto, UsuarioPerfil, Sabor, Inventario, EmailLog, Venta, VentaProducto

admin.site.register(Producto)
admin.site.register(UsuarioPerfil)
admin.site.register(Sabor)
admin.site.register(Inventario)
admin.site.register(EmailLog)
admin.site.register(Venta)
admin.site.register(VentaProducto)
