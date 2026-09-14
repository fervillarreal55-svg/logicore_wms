from django.core.management.base import BaseCommand
from inventario.models import Almacen, Zona, Ubicacion, Categoria, Unidad, Proveedor, Producto, Cliente, OrdenRecepcion, LineaRecepcion, PedidoDespacho, LineaDespacho
from inventario.services import registrar_movimiento

class Command(BaseCommand):
    help = 'Pobla todo el sistema LogiCore WMS: Almacén, Catálogo, Inventario, Recepción y Despacho'

    def handle(self, *args, **kwargs):
        # 1. MÓDULO ALMACÉN
        bodega, _ = Almacen.objects.get_or_create(nombre='Bodega Central Tulcán')
        
        z_recepcion, _ = Zona.objects.get_or_create(nombre='Zona de Recepción', almacen=bodega)
        z_almacenamiento, _ = Zona.objects.get_or_create(nombre='Zona de Almacenamiento', almacen=bodega)
        z_despacho, _ = Zona.objects.get_or_create(nombre='Zona de Despacho', almacen=bodega)
        
        ubicaciones_data = [
            ('A-01-01', z_almacenamiento, 100),
            ('A-01-02', z_almacenamiento, 100),
            ('A-02-01', z_almacenamiento, 150),
            ('A-02-02', z_almacenamiento, 150),
            ('B-01-01', z_almacenamiento, 120),
            ('B-01-02', z_almacenamiento, 120),
            ('B-02-01', z_almacenamiento, 200),
            ('B-02-02', z_almacenamiento, 200),
            ('C-01-01', z_almacenamiento, 130),
            ('C-01-02', z_almacenamiento, 130),
            ('REC-01-01', z_recepcion, 500),
            ('DES-01-01', z_despacho, 300),
        ]
        
        for codigo, zona, capacidad in ubicaciones_data:
            Ubicacion.objects.get_or_create(
                codigo=codigo,
                defaults={'zona': zona, 'capacidad': capacidad}
            )

        # 2. MÓDULO CATÁLOGO
        u_unidad, _ = Unidad.objects.get_or_create(nombre='Unidad', abreviatura='UND')
        c1, _ = Categoria.objects.get_or_create(nombre='Cómputo y Laptops', descripcion='Equipos portátiles')
        c2, _ = Categoria.objects.get_or_create(nombre='Smartphones y Móviles', descripcion='Dispositivos celulares')
        c3, _ = Categoria.objects.get_or_create(nombre='Audio y Periféricos', descripcion='Accesorios')
        
        p1, _ = Proveedor.objects.get_or_create(nombre='TechGlobal S.A.', defaults={'contacto': 'Juan Pérez', 'telefono': '0991234567'})
        p2, _ = Proveedor.objects.get_or_create(nombre='Distribuidores Andes C.A.', defaults={'contacto': 'María Andrade', 'telefono': '0987654321'})
        
        productos = [
            ('SKU-001', 'Laptop Lenovo ThinkPad E14', c1, p1),
            ('SKU-002', 'MacBook Pro 16 M3', c1, p1),
            ('SKU-003', 'Laptop HP Pavilion 15', c1, p2),
            ('SKU-004', 'Smartphone Samsung S24', c2, p2),
            ('SKU-005', 'iPhone 15 Pro Max', c2, p1),
            ('SKU-006', 'Xiaomi Redmi Note 13', c2, p2),
            ('SKU-007', 'Diadema Gamer HyperX', c3, p1),
            ('SKU-008', 'Teclado Mecánico RGB', c3, p2),
            ('SKU-009', 'Mouse Inalámbrico Logitech', c3, p1),
            ('SKU-010', 'Monitor LG UltraWide 29"', c3, p2),
        ]
        
        for sku, nombre, cat, prov in productos:
            Producto.objects.get_or_create(
                sku=sku,
                defaults={
                    'nombre': nombre,
                    'categoria': cat,
                    'unidad': u_unidad,
                    'proveedor': prov
                }
            )

        # 3. MÓDULO CLIENTES, RECEPCIÓN, DESPACHO E INVENTARIO
        cli1, _ = Cliente.objects.get_or_create(nombre='Comercial del Norte', defaults={'ruc': '1001234567001', 'telefono': '0981112223'})
        cli2, _ = Cliente.objects.get_or_create(nombre='Distribuciones Imbabura', defaults={'ruc': '1009876543001', 'telefono': '0993334445'})

        ub_alm = Ubicacion.objects.get(codigo='A-01-01')
        ub_alm2 = Ubicacion.objects.get(codigo='A-01-02')
        prod_1 = Producto.objects.get(sku='SKU-001')
        prod_2 = Producto.objects.get(sku='SKU-002')
        prod_3 = Producto.objects.get(sku='SKU-003')

        # Movimientos de inventario (Entrada, Traslado, Salida e Intento Fallido)
        registrar_movimiento('ENTRADA', prod_1, None, ub_alm, 50, 'LOTE-2026-A')
        registrar_movimiento('ENTRADA', prod_2, None, ub_alm, 30, 'LOTE-2026-B')
        
        # Intentar simular traslado y salida controlados
        try:
            registrar_movimiento('TRASLADO', prod_1, ub_alm, ub_alm2, 10, 'LOTE-2026-A')
        except Exception:
            pass

        try:
            registrar_movimiento('SALIDA', prod_1, ub_alm, None, 999, 'LOTE-2026-A') # Intento fallido por stock
        except Exception:
            pass

        # Órdenes de Recepción (2 órdenes con 3 líneas cada una)
        ord1, _ = OrdenRecepcion.objects.get_or_create(numero='OC-001', proveedor=p1, estado='COMPLETADA')
        LineaRecepcion.objects.get_or_create(orden=ord1, producto=prod_1, defaults={'cantidad_esperada': 10, 'cantidad_recibida': 10})
        LineaRecepcion.objects.get_or_create(orden=ord1, producto=prod_2, defaults={'cantidad_esperada': 15, 'cantidad_recibida': 15})
        LineaRecepcion.objects.get_or_create(orden=ord1, producto=prod_3, defaults={'cantidad_esperada': 20, 'cantidad_recibida': 20})

        ord2, _ = OrdenRecepcion.objects.get_or_create(numero='OC-002', proveedor=p2, estado='PENDIENTE')
        LineaRecepcion.objects.get_or_create(orden=ord2, producto=prod_1, defaults={'cantidad_esperada': 5, 'cantidad_recibida': 0})
        LineaRecepcion.objects.get_or_create(orden=ord2, producto=prod_2, defaults={'cantidad_esperada': 8, 'cantidad_recibida': 0})
        LineaRecepcion.objects.get_or_create(orden=ord2, producto=prod_3, defaults={'cantidad_esperada': 12, 'cantidad_recibida': 0})

        # Pedidos de Despacho (2 pedidos con 3 líneas cada uno)
        ped1, _ = PedidoDespacho.objects.get_or_create(numero='PED-001', cliente=cli1, prioridad='ALTA', estado='APROBADO')
        LineaDespacho.objects.get_or_create(pedido=ped1, producto=prod_1, defaults={'cantidad': 2})
        LineaDespacho.objects.get_or_create(pedido=ped1, producto=prod_2, defaults={'cantidad': 3})
        LineaDespacho.objects.get_or_create(pedido=ped1, producto=prod_3, defaults={'cantidad': 1})

        ped2, _ = PedidoDespacho.objects.get_or_create(numero='PED-002', cliente=cli2, prioridad='NORMAL', estado='PENDIENTE')
        LineaDespacho.objects.get_or_create(pedido=ped2, producto=prod_1, defaults={'cantidad': 4})
        LineaDespacho.objects.get_or_create(pedido=ped2, producto=prod_2, defaults={'cantidad': 5})
        LineaDespacho.objects.get_or_create(pedido=ped2, producto=prod_3, defaults={'cantidad': 2})

        self.stdout.write(self.style.SUCCESS('¡SISTEMA LOGICORE WMS COMPLETAMENTE POBLADO Y FUNCIONAL!'))