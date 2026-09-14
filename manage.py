#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logicore_core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


# Bloque temporal para poblar el WMS de LogiCore UPEC con los datos exactos
def poblar_automatico():
    try:
        from inventario.models import Almacen, Zona, Ubicacion, Categoria, Unidad, Proveedor, Producto
        
        u_unidad, _ = Unidad.objects.get_or_create(nombre='Unidad', abreviatura='UND')
        c1, _ = Categoria.objects.get_or_create(nombre='Cómputo y Laptops', descripcion='Equipos portátiles')
        c2, _ = Categoria.objects.get_or_create(nombre='Smartphones y Móviles', descripcion='Dispositivos celulares')
        c3, _ = Categoria.objects.get_or_create(nombre='Audio y Periféricos', descripcion='Accesorios')
        
        p1, _ = Proveedor.objects.get_or_create(nombre='TechGlobal S.A.', defaults={'contacto': 'Juan Pérez', 'telefono': '0991234567'})
        p2, _ = Proveedor.objects.get_or_create(nombre='Distribuidores Andes C.A.', defaults={'contacto': 'María Andrade', 'telefono': '0987654321'})
        
        alm, _ = Almacen.objects.get_or_create(nombre='Almacén Principal Tulcán', defaults={'direccion': 'Av. Panamericana'})
        z, _ = Zona.objects.get_or_create(nombre='Zona General', almacen=alm)
        ub, _ = Ubicacion.objects.get_or_create(codigo='A-01-01', zona=z, descripcion='Rack Principal')
        
        productos = [
            ('Laptop Lenovo ThinkPad E14', c1, p1, 25, 750.0),
            ('MacBook Pro 16 M3', c1, p1, 12, 2200.0),
            ('Laptop HP Pavilion 15', c1, p2, 15, 680.0),
            ('Smartphone Samsung S24', c2, p2, 30, 1100.0),
            ('iPhone 15 Pro Max', c2, p1, 18, 1300.0),
            ('Xiaomi Redmi Note 13', c2, p2, 40, 280.0),
            ('Diadema Gamer HyperX', c3, p1, 45, 65.0),
            ('Teclado Mecánico RGB', c3, p2, 50, 45.0),
            ('Mouse Inalámbrico Logitech', c3, p1, 35, 90.0),
            ('Monitor LG UltraWide 29"', c3, p2, 20, 310.0),
        ]
        
        for nombre, cat, prov, stock, precio in productos:
            Producto.objects.get_or_create(
                nombre=nombre,
                defaults={'categoria': cat, 'unidad': u_unidad, 'proveedor': prov, 'stock': stock, 'precio': precio, 'ubicacion': ub}
            )
        print("¡ÉXITO TOTAL: 10 productos, 3 categorías y 2 proveedores registrados en la base de datos!")
    except Exception as e:
        print(f"Aviso de ejecución: {e}")


if __name__ == '__main__':
    # Si ejecutamos 'python manage.py runserver' u otro comando normal, corre Django.
    # Si ejecutamos solo 'python manage.py', aprovecha para poblar los datos automáticamente.
    if len(sys.argv) == 1:
        poblar_automatico()
    main()