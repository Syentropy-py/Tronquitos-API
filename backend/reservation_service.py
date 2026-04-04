"""
Servicio de Lógica de Negocio para Reservas
Maneja la disponibilidad de mesas, validaciones y operaciones de reservas
"""

from datetime import datetime, timedelta
import database as db
from models import TableStatus, ReservationStatus, EventType


class ReservationService:
    """Servicio encargado de la lógica de reservas y mesas"""
    
    @staticmethod
    def find_available_table(people_count, fecha, hora, sede='Centro'):
        """
        Encuentra una mesa disponible para una reserva en una sede específica.
        
        Args:
            people_count (int): Número de personas
            fecha (str): Fecha en formato YYYY-MM-DD
            hora (str): Hora en formato HH:MM
            sede (str): Nombre de la sede (Centro, Usaquén, Chapinero)
        
        Returns:
            dict: Mesa disponible o None si no hay disponibilidad
        """
        available_tables = db.get_available_tables(people_count, fecha, hora, sede)
        
        if available_tables:
            # Retorna la mesa con menor capacidad que acomode al grupo
            # (optimiza uso del espacio)
            return dict(available_tables[0])
        
        return None
    
    @staticmethod
    def create_reservation(nombre, telefono, email, personas, fecha, hora, sede='Centro', mensaje=''):
        """
        Crea una nueva reserva en una sede específica.
        
        Lógica:
        1. Valida que la reserva sea futura
        2. Si personas > 30: crea reserva grupal especial (sin necesidad de mesa específica)
        3. Si personas <= 30: busca una mesa disponible
        4. Crea evento en BD para auditoría
        
        Args:
            nombre (str): Nombre del cliente
            telefono (str): Teléfono del cliente
            email (str): Email del cliente
            personas (int): Número de personas
            fecha (str): Fecha en formato YYYY-MM-DD
            hora (str): Hora en formato HH:MM
            sede (str): Nombre de la sede (Centro, Usaquén, Chapinero)
            mensaje (str): Mensaje o notas adicionales
        
        Returns:
            dict: {
                'success': bool,
                'message': str,
                'reservation_id': int (si success=True),
                'is_special_group': bool,
                'table_number': int o None (si success=True)
            }
        """
        
        # Validar que la fecha/hora sea futura
        try:
            reservation_datetime = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
            if reservation_datetime < datetime.now():
                return {
                    'success': False,
                    'message': 'No se puede crear una reserva en el pasado'
                }
        except ValueError:
            return {
                'success': False,
                'message': 'Formato de fecha u hora inválido'
            }
        
        # Detectar si es un grupo especial (> 30 personas)
        is_special_group = personas > 30
        
        if is_special_group:
            # Para grupos especiales, NO necesita mesa específica
            # Se crea la reserva sin asignar mesa
            try:
                reservation_id = db.create_reservation(
                    nombre, telefono, email, personas, fecha, hora, 
                    tabla_id=None, sede=sede, mensaje=mensaje, is_special_group=1
                )
                
                # Crear evento para auditoría
                db.create_event(
                    EventType.RESERVATION_CREATED,
                    reservation_id=reservation_id,
                    table_id=None,
                    description=f'⭐ RESERVA GRUPAL ESPECIAL: {personas} personas - Requiere confirmación manual'
                )
                
                return {
                    'success': True,
                    'message': f'✅ Reserva grupal especial registrada ({personas} personas). El restaurante confirmará los detalles por teléfono.',
                    'reservation_id': reservation_id,
                    'is_special_group': True,
                    'table_number': None,
                    'note': 'El gerente del restaurante contactará para confirmar disponibilidad de espacio y detalles.'
                }
            
            except Exception as e:
                return {
                    'success': False,
                    'message': f'Error al crear reserva grupal: {str(e)}'
                }
        
        else:
            # Para grupos normales (<= 30), buscar mesa disponible
            table = ReservationService.find_available_table(personas, fecha, hora, sede)
            
            if not table:
                return {
                    'success': False,
                    'message': f'No hay mesas disponibles para {personas} personas en esa fecha/hora'
                }
            
            try:
                # Crear reserva con mesa asignada
                reservation_id = db.create_reservation(
                    nombre, telefono, email, personas, fecha, hora, table['id'], sede, mensaje
                )
                
                # Actualizar estado de mesa a 'reserved'
                db.update_table_status(table['id'], TableStatus.RESERVED)
                
                # Crear evento para auditoría
                db.create_event(
                    EventType.RESERVATION_CREATED,
                    reservation_id=reservation_id,
                    table_id=table['id'],
                    description=f'Reserva creada para {personas} personas en mesa {table["table_number"]}'
                )
                
                return {
                    'success': True,
                    'message': 'Reserva creada exitosamente',
                    'reservation_id': reservation_id,
                    'is_special_group': False,
                    'table_number': table['table_number']
                }
            
            except Exception as e:
                return {
                    'success': False,
                    'message': f'Error al crear la reserva: {str(e)}'
                }
    
    @staticmethod
    def cancel_reservation(reservation_id):
        """
        Cancela una reserva y libera la mesa asociada.
        
        Args:
            reservation_id (int): ID de la reserva a cancelar
        
        Returns:
            dict: {
                'success': bool,
                'message': str,
                'table_id': int (si success=True)
            }
        """
        try:
            reservation = db.get_reservation(reservation_id)
            
            if not reservation:
                return {
                    'success': False,
                    'message': 'Reserva no encontrada'
                }
            
            if reservation['status'] == ReservationStatus.CANCELLED:
                return {
                    'success': False,
                    'message': 'La reserva ya estaba cancelada'
                }
            
            # Cancelar reserva
            db.cancel_reservation(reservation_id)
            
            # Crear evento
            db.create_event(
                EventType.RESERVATION_CANCELLED,
                reservation_id=reservation_id,
                table_id=reservation['table_id'],
                description=f'Reserva cancelada por {reservation["nombre"]}'
            )
            
            return {
                'success': True,
                'message': 'Reserva cancelada y mesa liberada',
                'table_id': reservation['table_id']
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al cancelar la reserva: {str(e)}'
            }
    
    @staticmethod
    def free_table(table_id):
        """
        Libera manualmente una mesa.
        
        Args:
            table_id (int): ID de la mesa
        
        Returns:
            dict: {'success': bool, 'message': str}
        """
        try:
            table = db.get_table(table_id)
            
            if not table:
                return {'success': False, 'message': 'Mesa no encontrada'}
            
            if table['status'] == TableStatus.FREE:
                return {'success': False, 'message': 'La mesa ya estaba libre'}
            
            # Liberar mesa
            db.update_table_status(table_id, TableStatus.FREE)
            
            # Crear evento
            db.create_event(
                EventType.TABLE_FREED,
                table_id=table_id,
                description=f'Mesa {table["table_number"]} liberada manualmente'
            )
            
            return {'success': True, 'message': f'Mesa {table["table_number"]} liberada'}
        
        except Exception as e:
            return {'success': False, 'message': f'Error al liberar la mesa: {str(e)}'}
    
    @staticmethod
    def check_and_release_late_reservations(minutes_late=20):
        """
        Verifica reservas que están más de X minutos tarde y las marca como no-show,
        liberando automáticamente sus mesas.
        
        Esta función debería ejecutarse periódicamente (ej: cada 5 minutos) mediante
        un scheduled job o cron task.
        
        Args:
            minutes_late (int): Minutos de retraso permitidos
        
        Returns:
            dict: {
                'success': bool,
                'released_reservations': int,
                'message': str
            }
        """
        try:
            late_reservations = db.get_late_reservations(minutes_late)
            released_count = 0
            
            for reservation in late_reservations:
                db.mark_no_show(reservation['id'])
                
                db.create_event(
                    EventType.NO_SHOW,
                    reservation_id=reservation['id'],
                    table_id=reservation['table_id'],
                    description=f'Reserva marcada como no-show ({minutes_late} min tarde)'
                )
                
                released_count += 1
            
            return {
                'success': True,
                'released_reservations': released_count,
                'message': f'{released_count} reserva(s) marcada(s) como no-show y mesa(s) liberada(s)'
            }
        
        except Exception as e:
            return {
                'success': False,
                'released_reservations': 0,
                'message': f'Error: {str(e)}'
            }
    
    @staticmethod
    def get_availability_summary(fecha):
        """
        Obtiene un resumen de disponibilidad para una fecha específica.
        
        Args:
            fecha (str): Fecha en formato YYYY-MM-DD
        
        Returns:
            dict: {
                'fecha': str,
                'total_tables': int,
                'available_tables': int,
                'reserved_tables': int,
                'occupied_tables': int,
                'reservations': [...]
            }
        """
        try:
            all_tables = db.get_all_tables()
            reservations = db.get_reservations_by_date(fecha)
            
            available = sum(1 for t in all_tables if t['status'] == TableStatus.FREE)
            reserved = sum(1 for t in all_tables if t['status'] == TableStatus.RESERVED)
            occupied = sum(1 for t in all_tables if t['status'] == TableStatus.OCCUPIED)
            
            return {
                'fecha': fecha,
                'total_tables': len(all_tables),
                'available_tables': available,
                'reserved_tables': reserved,
                'occupied_tables': occupied,
                'reservations': [dict(r) for r in reservations]
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
