from django.core.exceptions import ValidationError
from .models import Existencia, MovimientoInventario

def registrar_movimiento(tipo, producto, ubicacion_origen, ubicacion_destino, cantidad, lote):
    """
    Gestiona de forma centralizada las entradas, salidas y traslados.
    Valida stock insuficiente y registra intentos fallidos.
    """
    if tipo in ['SALIDA', 'TRASLADO']:
        try:
            existencia_orig = Existencia.objects.get(
                producto=producto, 
                ubicacion=ubicacion_origen, 
                lote=lote
            )
            if existencia_orig.cantidad < cantidad:
                # Registrar intento fallido obligatorio
                MovimientoInventario.objects.create(
                    tipo='INTENTO_FALLIDO',
                    producto=producto,
                    cantidad=cantidad,
                    detalles=f"Fallo por stock insuficiente. Disponible: {existencia_orig.cantidad}"
                )
                raise ValidationError("Stock insuficiente para completar la operación.")
        except Existencia.DoesNotExist:
            MovimientoInventario.objects.create(
                tipo='INTENTO_FALLIDO',
                producto=producto,
                cantidad=cantidad,
                detalles="Fallo por ausencia de existencia en origen/lote."
            )
            raise ValidationError("No existe inventario registrado en la ubicación de origen para este lote.")

    # Si es ENTRADA
    if tipo == 'ENTRADA':
        existencia_dest, _ = Existencia.objects.get_or_create(
            producto=producto,
            ubicacion=ubicacion_destino,
            lote=lote,
            defaults={'cantidad': 0}
        )
        existencia_dest.cantidad += cantidad
        existencia_dest.save()

    # Registrar el movimiento de solo lectura
    MovimientoInventario.objects.create(
        tipo=tipo,
        producto=producto,
        cantidad=cantidad,
        detalles=f"Movimiento de {tipo} exitoso por servicios."
    )