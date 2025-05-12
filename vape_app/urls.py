from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Admin Dashboard
    path('admin-view/', views.admin_dashboard, name='admin_dashboard'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('sabor/<int:sabor_id>/productos/', views.get_productos_por_sabor, name='get_productos_por_sabor'),
    path('sabores/', views.sabor_list, name='sabor_list'),
    path('sabores/crear/', views.sabor_create, name='sabor_create'),
    path('sabores/editar/<int:pk>/', views.sabor_edit, name='sabor_edit'),
    path('sabores/eliminar/<int:pk>/', views.sabor_delete, name='sabor_delete'),
    
    # Product URLs
    path('productos/', views.producto_list, name='producto_list'),
    path('productos/crear/', views.producto_create, name='producto_create'),
    path('productos/editar/<int:pk>/', views.producto_edit, name='producto_edit'),
    path('productos/eliminar/<int:pk>/', views.producto_delete, name='producto_delete'),
    
        # Inventory URLs
    path('inventarios/', views.inventario_list, name='inventario_list'),
    path('inventarios/crear/', views.inventario_create, name='inventario_create'),
    path('inventarios/editar/<int:pk>/', views.inventario_edit, name='inventario_edit'),
    path('inventarios/eliminar/<int:pk>/', views.inventario_delete, name='inventario_delete'),

     # New URLs for Cliente and Venta
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/create/', views.cliente_create, name='cliente_create'),
    path('clientes/edit/<int:pk>/', views.cliente_edit, name='cliente_edit'),
    path('clientes/delete/<int:pk>/', views.cliente_delete, name='cliente_delete'),
    path('ventas/', views.venta_list, name='venta_list'),
    path('ventas/create/', views.venta_create, name='venta_create'),
    path('ventas/edit/<int:pk>/', views.venta_edit, name='venta_edit'),
    path('ventas/delete/<int:pk>/', views.venta_delete, name='venta_delete'),
    path('ventas/detail/<int:pk>/', views.venta_detail, name='venta_detail'),
    
    # AJAX URL for Products Modal
    path('sabores/<int:sabor_id>/productos/', views.get_productos_by_sabor, name='get_productos_by_sabor'),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)