/**
 * CONFIGURACIÓN DE SEDES - LOS TRONQUITOS
 * 
 * Fácil de editar sin tocar el HTML
 * Horarios por sede y día de la semana
 * 
 * DÍAS: 0=Lunes, 1=Martes, 2=Miércoles, 3=Jueves, 4=Viernes, 5=Sábado, 6=Domingo
 */

const SEDES = [
  {
    id: 'principal',
    nombre: 'Sede Principal',
    barrio: 'Barrio Camelia',
    direccion: 'Av. Calle 3 #53-07',
    ciudad: 'Bogotá',
    telefono: '414 68 70',
    maps_url: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3976.8!2d-74.1152934!3d4.6152116!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x8e3f994efe4857e9%3A0x84eb606e99903a46!2sASADERO%20LOS%20TRONQUITOS!5e0!3m2!1ses!2sco!4v1709600000000!5m2!1ses!2sco',
    horarios: {
      0: { abre: '11:30', cierra: '18:00' }, // Lunes
      1: { abre: '11:30', cierra: '18:00' }, // Martes
      2: { abre: '11:30', cierra: '18:00' }, // Miércoles
      3: { abre: '11:30', cierra: '18:00' }, // Jueves
      4: { abre: '11:30', cierra: '21:00' }, // Viernes
      5: { abre: '11:30', cierra: '21:00' }, // Sábado
      6: { abre: '11:30', cierra: '19:00' }  // Domingo
    }
  },
  {
    id: 'terraza',
    nombre: 'Sede Terraza',
    barrio: 'Terraza',
    direccion: 'Cra 7 #19-74',
    ciudad: 'Bogotá',
    telefono: '414 68 70',
    maps_url: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3976.8!2d-74.11!3d4.63!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!5e0!3m2!1ses!2sco!4v1709600000000!5m2!1ses!2sco',
    horarios: {
      0: { abre: '11:30', cierra: '18:00' }, // Lunes
      1: { abre: '11:30', cierra: '18:00' }, // Martes
      2: { abre: '11:30', cierra: '18:00' }, // Miércoles
      3: { abre: '11:30', cierra: '18:00' }, // Jueves
      4: { abre: '11:30', cierra: '18:00' }, // Viernes
      5: { abre: '11:30', cierra: '18:00' }, // Sábado
      6: { abre: '11:30', cierra: '19:00' }  // Domingo
    }
  },
  {
    id: 'restrepo',
    nombre: 'Sede Restrepo',
    barrio: 'Restrepo',
    direccion: 'Cl 15 Sur #22-20',
    ciudad: 'Bogotá',
    telefono: '414 68 70',
    maps_url: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3976.8!2d-74.12!3d4.60!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!5e0!3m2!1ses!2sco!4v1709600000000!5m2!1ses!2sco',
    horarios: {
      0: { abre: '11:30', cierra: '18:00' }, // Lunes
      1: { abre: '11:30', cierra: '18:00' }, // Martes
      2: { abre: '11:30', cierra: '18:00' }, // Miércoles
      3: { abre: '11:30', cierra: '18:00' }, // Jueves
      4: { abre: '11:30', cierra: '18:00' }, // Viernes
      5: { abre: '11:30', cierra: '18:00' }, // Sábado
      6: { abre: '11:30', cierra: '19:00' }  // Domingo
    }
  },
  {
    id: 'nieves',
    nombre: 'Sede Nieves',
    barrio: 'Nieves',
    direccion: 'Cra 7 #19-74',
    ciudad: 'Bogotá',
    telefono: '414 68 70',
    maps_url: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3976.8!2d-74.11!3d4.62!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!5e0!3m2!1ses!2sco!4v1709600000000!5m2!1ses!2sco',
    horarios: {
      0: { abre: '11:30', cierra: '18:00' }, // Lunes
      1: { abre: '11:30', cierra: '18:00' }, // Martes
      2: { abre: '11:30', cierra: '18:00' }, // Miércoles
      3: { abre: '11:30', cierra: '18:00' }, // Jueves
      4: { abre: '11:30', cierra: '18:00' }, // Viernes
      5: { abre: '11:30', cierra: '18:00' }, // Sábado
      6: { abre: '11:30', cierra: '19:00' }  // Domingo
    }
  },
  {
    id: '7ma-con-22',
    nombre: 'Sede 7ma con 22',
    barrio: '7ma con 22',
    direccion: 'Cra 7 #22-12',
    ciudad: 'Bogotá',
    telefono: '414 68 70',
    maps_url: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3976.8!2d-74.11!3d4.61!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!5e0!3m2!1ses!2sco!4v1709600000000!5m2!1ses!2sco',
    horarios: {
      0: { abre: '11:30', cierra: '19:00' }, // Lunes
      1: { abre: '11:30', cierra: '19:00' }, // Martes
      2: { abre: '11:30', cierra: '19:00' }, // Miércoles
      3: { abre: '11:30', cierra: '19:00' }, // Jueves
      4: { abre: '11:30', cierra: '19:00' }, // Viernes
      5: { abre: '11:30', cierra: '19:00' }, // Sábado
      6: { abre: '11:30', cierra: '19:00' }  // Domingo
    }
  },
  {
    id: 'rojas',
    nombre: 'Sede Av. Rojas',
    barrio: 'Av. Rojas',
    direccion: 'Av. Rojas #3-08',
    ciudad: 'Bogotá',
    telefono: '414 68 70',
    maps_url: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3024.1234567890!2d-74.0059!3d40.7128!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!5e0!3m2!1ses!2sco!4v1234567890',
    horarios: {
      0: { abre: '11:30', cierra: '18:00' }, // Lunes
      1: { abre: '11:30', cierra: '18:00' }, // Martes
      2: { abre: '11:30', cierra: '18:00' }, // Miércoles
      3: { abre: '11:30', cierra: '18:00' }, // Jueves
      4: { abre: '11:30', cierra: '18:00' }, // Viernes
      5: { abre: '11:30', cierra: '19:00' }, // Sábado
      6: { abre: '11:30', cierra: '19:00' }  // Domingo
    }
  }
];

/**
 * FUNCIONES DE UTILIDAD PARA HORARIOS
 */

// Obtener horario de una sede para un día específico
function getHorarioSede(sedeId, dia = null) {
  if (dia === null) {
    // Si no se especifica día, usar el día actual
    // Nota: JavaScript usa 0=Domingo, pero nosotros usamos 0=Lunes
    let hoy = new Date().getDay();
    dia = hoy === 0 ? 6 : hoy - 1; // Convertir formato de JS a nuestro formato
  }
  
  const sede = SEDES.find(s => s.id === sedeId);
  if (!sede) return null;
  
  return sede.horarios[dia];
}

// Obtener sede por ID
function getSede(sedeId) {
  return SEDES.find(s => s.id === sedeId);
}

// Convertir hora 24h a formato 12h
function formatHour12h(hora24) {
  const [h, m] = hora24.split(':').map(Number);
  const ampm = h >= 12 ? 'PM' : 'AM';
  const hh = h > 12 ? h - 12 : (h === 0 ? 12 : h);
  return `${hh}:${String(m).padStart(2, '0')} ${ampm}`;
}

// Obtener nombre del día
function getNombreDia(dia) {
  const dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
  return dias[dia];
}

// Obtener tutti los horarios de una sede
function getHorariosSede(sedeId) {
  const sede = getSede(sedeId);
  if (!sede) return null;
  
  const horarios = {};
  for (let dia = 0; dia < 7; dia++) {
    const h = sede.horarios[dia];
    horarios[getNombreDia(dia)] = {
      abre: formatHour12h(h.abre),
      cierra: formatHour12h(h.cierra)
    };
  }
  return horarios;
}
