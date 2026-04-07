/* ============================================================
   ASADERO LOS TRONQUITOS — JavaScript
   Interactive functionality: carousel, lightbox, forms, animations
   ============================================================ */

/* Convertir hora de 12 horas a 24 horas */
function convertTo24Hour(timeString) {
  if (!timeString) return '20:00'; // Default time
  
  // Parse "12:00 pm" or "12:00 am"
  const [time, period] = timeString.split(' ');
  let [hours, minutes] = time.split(':').map(Number);
  
  if (period.toLowerCase() === 'pm' && hours !== 12) {
    hours += 12;
  } else if (period.toLowerCase() === 'am' && hours === 12) {
    hours = 0;
  }
  
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
}

/* Convertir rango de personas a número */
function extractPersonas(personasText) {
  if (!personasText) return 1;
  
  // Casos especiales
  if (personasText.includes('30+')) return 30;  // "30+ personas" → 30
  
  // Extraer números del rango (ej: "1-2 personas" → 2, "16-30 personas" → 30)
  const numbers = personasText.match(/\d+/g);
  
  if (numbers && numbers.length > 0) {
    // Usar el número más alto del rango
    return parseInt(numbers[numbers.length - 1]);
  }
  
  return 1; // Default fallback
}

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  /* ── 1. STICKY HEADER ── */
  const header = document.getElementById('header');
  const handleScroll = () => {
    header.classList.toggle('header--scrolled', window.scrollY > 80);
    // Back to top button
    const btn = document.getElementById('backToTop');
    if (btn) btn.classList.toggle('back-to-top--visible', window.scrollY > 600);
  };
  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();

  /* ── 2. MOBILE MENU ── */
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobileMenu');
  
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('hamburger--active');
      mobileMenu.classList.toggle('mobile-menu--open');
      document.body.style.overflow = mobileMenu.classList.contains('mobile-menu--open') ? 'hidden' : '';
    });

    // Close mobile menu on link click
    mobileMenu.querySelectorAll('.mobile-menu__link').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('hamburger--active');
        mobileMenu.classList.remove('mobile-menu--open');
        document.body.style.overflow = '';
      });
    });
  }

  /* ── 3. SMOOTH SCROLL with active nav highlighting ── */
  const navLinks = document.querySelectorAll('.nav__link');
  const sections = document.querySelectorAll('section[id]');

  // Active section highlighting on scroll
  const observerOptions = { rootMargin: '-20% 0px -80% 0px' };
  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        navLinks.forEach(link => {
          link.classList.toggle('nav__link--active', link.getAttribute('href') === `#${id}`);
        });
      }
    });
  }, observerOptions);

  sections.forEach(section => sectionObserver.observe(section));

  /* ── 4. HERO CAROUSEL ── */
  const slides = document.querySelectorAll('.hero__slide');
  const dots = document.querySelectorAll('.hero__dot');
  let currentSlide = 0;
  let heroInterval;

  function goToSlide(n) {
    slides[currentSlide].classList.remove('hero__slide--active');
    dots[currentSlide].classList.remove('hero__dot--active');
    currentSlide = (n + slides.length) % slides.length;
    slides[currentSlide].classList.add('hero__slide--active');
    dots[currentSlide].classList.add('hero__dot--active');
  }

  function startHeroAutoplay() {
    heroInterval = setInterval(() => goToSlide(currentSlide + 1), 5000);
  }

  if (slides.length > 0) {
    dots.forEach(dot => {
      dot.addEventListener('click', () => {
        clearInterval(heroInterval);
        goToSlide(parseInt(dot.dataset.slide));
        startHeroAutoplay();
      });
    });
    startHeroAutoplay();
  }

  /* ── 5. MENU TABS ── */
  const menuTabs = document.querySelectorAll('.menu__tab');
  const menuItems = document.querySelectorAll('.menu__item[data-category]');

  menuTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Update active tab
      menuTabs.forEach(t => t.classList.remove('menu__tab--active'));
      tab.classList.add('menu__tab--active');

      const filter = tab.dataset.filter;

      menuItems.forEach(item => {
        if (filter === 'all' || item.dataset.category === filter) {
          item.classList.add('show');
          item.style.animation = 'fadeInUp 0.4s ease forwards';
        } else {
          item.classList.remove('show');
        }
      });
    });
  });

  // Add fadeInUp animation
  const style = document.createElement('style');
  style.textContent = `
    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(15px); }
      to { opacity: 1; transform: translateY(0); }
    }
  `;
  document.head.appendChild(style);

  /* ── 6. GALLERY LIGHTBOX ── */
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = lightbox ? lightbox.querySelector('.lightbox__img') : null;
  const galleryItems = document.querySelectorAll('[data-lightbox]');
  let lightboxImages = [];
  let lightboxIndex = 0;

  if (lightbox && galleryItems.length > 0) {
    // Collect all gallery image sources
    galleryItems.forEach((item, i) => {
      const img = item.querySelector('img');
      if (img) {
        lightboxImages.push(img.src);
        item.addEventListener('click', () => openLightbox(i));
      }
    });

    function openLightbox(index) {
      lightboxIndex = index;
      lightboxImg.src = lightboxImages[lightboxIndex];
      lightbox.classList.add('lightbox--open');
      document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
      lightbox.classList.remove('lightbox--open');
      document.body.style.overflow = '';
    }

    lightbox.querySelector('.lightbox__close').addEventListener('click', closeLightbox);
    lightbox.querySelector('.lightbox__nav--prev').addEventListener('click', (e) => {
      e.stopPropagation();
      lightboxIndex = (lightboxIndex - 1 + lightboxImages.length) % lightboxImages.length;
      lightboxImg.src = lightboxImages[lightboxIndex];
    });
    lightbox.querySelector('.lightbox__nav--next').addEventListener('click', (e) => {
      e.stopPropagation();
      lightboxIndex = (lightboxIndex + 1) % lightboxImages.length;
      lightboxImg.src = lightboxImages[lightboxIndex];
    });
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) closeLightbox();
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (!lightbox.classList.contains('lightbox--open')) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') {
        lightboxIndex = (lightboxIndex - 1 + lightboxImages.length) % lightboxImages.length;
        lightboxImg.src = lightboxImages[lightboxIndex];
      }
      if (e.key === 'ArrowRight') {
        lightboxIndex = (lightboxIndex + 1) % lightboxImages.length;
        lightboxImg.src = lightboxImages[lightboxIndex];
      }
    });
  }

  /* ── 7. TESTIMONIALS SLIDER ── */
  const testimonialsTrack = document.getElementById('testimonialsTrack');
  const testimonialsDots = document.getElementById('testimonialsDots');
  
  if (testimonialsTrack && testimonialsDots) {
    const testimonialSlides = testimonialsTrack.querySelectorAll('.testimonials__slide');
    let currentTestimonial = 0;
    let testimonialInterval;

    // Create dots
    testimonialSlides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.classList.add('testimonials__dot');
      if (i === 0) dot.classList.add('testimonials__dot--active');
      dot.addEventListener('click', () => goToTestimonial(i));
      testimonialsDots.appendChild(dot);
    });

    const tDots = testimonialsDots.querySelectorAll('.testimonials__dot');

    function goToTestimonial(n) {
      tDots[currentTestimonial].classList.remove('testimonials__dot--active');
      currentTestimonial = (n + testimonialSlides.length) % testimonialSlides.length;
      tDots[currentTestimonial].classList.add('testimonials__dot--active');
      testimonialsTrack.style.transform = `translateX(-${currentTestimonial * 100}%)`;
    }

    function startTestimonialAutoplay() {
      testimonialInterval = setInterval(() => goToTestimonial(currentTestimonial + 1), 6000);
    }

    startTestimonialAutoplay();

    // Pause on hover
    testimonialsTrack.addEventListener('mouseenter', () => clearInterval(testimonialInterval));
    testimonialsTrack.addEventListener('mouseleave', startTestimonialAutoplay);
  }

  /* ── 7.5 SEDES SLIDERS (dos grupos de 3 sedes) ── */
  function initSedesSlider(trackId, dotsId) {
    const sedesTrack = document.getElementById(trackId);
    const sedesDots = document.getElementById(dotsId);
    
    if (!sedesTrack || !sedesDots) return;
    
    const sedesSlides = sedesTrack.querySelectorAll('.contact__card');
    let currentSede = 0;
    let sedeInterval;

    // Create dots
    sedesSlides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.classList.add('contact__dot');
      if (i === 0) dot.classList.add('contact__dot--active');
      dot.addEventListener('click', () => goToSede(i));
      sedesDots.appendChild(dot);
    });

    const sDots = sedesDots.querySelectorAll('.contact__dot');

    function goToSede(n) {
      sDots[currentSede].classList.remove('contact__dot--active');
      currentSede = (n + sedesSlides.length) % sedesSlides.length;
      sDots[currentSede].classList.add('contact__dot--active');
      sedesTrack.style.transform = `translateX(-${currentSede * 100}%)`;
    }

    function startSedeAutoplay() {
      sedeInterval = setInterval(() => goToSede(currentSede + 1), 6000);
    }

    startSedeAutoplay();

    // Pause on hover
    sedesTrack.addEventListener('mouseenter', () => clearInterval(sedeInterval));
    sedesTrack.addEventListener('mouseleave', startSedeAutoplay);
  }

  // Initialize both sliders
  initSedesSlider('sedesTrack1', 'sedesDots1');
  initSedesSlider('sedesTrack2', 'sedesDots2');

  /* ── 7.6 UPDATE HORARIOS DINAMICALLY ── */
  function updateHorariosDinamicos() {
    // Get today's day (0=Monday, 6=Sunday)
    const today = new Date();
    const diaSemana = today.getDay();
    // Adjust: JS getDay returns 0=Sunday, but we use 0=Monday
    const dia = diaSemana === 0 ? 6 : diaSemana - 1;
    
    // Update horarios for each sede
    document.querySelectorAll('[data-sede]').forEach(card => {
      const sedeId = card.getAttribute('data-sede');
      if (!window.SEDES) return;
      
      const sede = window.SEDES.find(s => s.id === sedeId);
      if (!sede) return;
      
      const horario = sede.horarios[dia];
      if (!horario) return;
      
      // Find and update the horario span
      const horarioSpan = card.querySelector('.sede-horario');
      if (horarioSpan) {
        const hora12 = formatHour12h(horario.abre);
        const cierra12 = formatHour12h(horario.cierra);
        horarioSpan.textContent = `${hora12} - ${cierra12}`;
      }
    });
  }

  // Helper function to format time
  function formatHour12h(hora24) {
    const [h, m] = hora24.split(':');
    let hNum = parseInt(h);
    const pm = hNum >= 12;
    if (hNum > 12) hNum -= 12;
    if (hNum === 0) hNum = 12;
    return `${hNum}:${m} ${pm ? 'PM' : 'AM'}`;
  }

  // Update on page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateHorariosDinamicos);
  } else {
    updateHorariosDinamicos();
  }

  /* ── 8. FORM VALIDATION ── */
  function validateForm(formId, fields) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let isValid = true;

      fields.forEach(field => {
        const input = document.getElementById(field.id);
        const error = document.getElementById(field.errorId);
        if (!input || !error) return;

        // Reset
        input.classList.remove('error');
        error.classList.remove('show');

        // Validate required
        if (field.required && !input.value.trim()) {
          input.classList.add('error');
          error.classList.add('show');
          isValid = false;
          return;
        }

        // Validate email
        if (field.type === 'email' && input.value.trim()) {
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailRegex.test(input.value)) {
            input.classList.add('error');
            error.classList.add('show');
            isValid = false;
          }
        }

        // Validate phone
        if (field.type === 'tel' && input.value.trim()) {
          const phoneRegex = /^[\d\s\-\+\(\)]{7,15}$/;
          if (!phoneRegex.test(input.value)) {
            input.classList.add('error');
            error.classList.add('show');
            isValid = false;
          }
        }

        // Validate future date
        if (field.type === 'date' && input.value) {
          const selectedDate = new Date(input.value);
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          if (selectedDate < today) {
            input.classList.add('error');
            error.classList.add('show');
            isValid = false;
          }
        }
      });

      if (isValid) {
        const submitBtn = form.querySelector('.form__submit');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Enviando...';
        submitBtn.disabled = true;

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        // Convertir "Personas" de texto/rango a número (ej: "1-2 personas" → 2, "30+ personas" → 30)
        const personasText = data.Personas;
        if (personasText) {
          data.Personas = extractPersonas(personasText);
        }

        // Convertir "Hora" de 12 horas a 24 horas (ej: "8:00 pm" → "20:00")
        const horaText = data.Hora;
        if (horaText) {
          data.Hora = convertTo24Hour(horaText);
        }

        // Si no hay sede en el form, usar "Centro" como default
        if (!data.Sede) {
          data.Sede = 'Centro';
        }

        console.log('[*] Datos antes de enviar:', data);

        fetch('/api/reservation', {
          method: 'POST',
          body: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        }).then(response => {
          if (response.ok) {
            const modal = document.getElementById('successModal');
            if (modal) {
              modal.querySelector('.modal__title').textContent = '¡Reservación Enviada!';
              modal.querySelector('.modal__text').textContent = 'Hemos recibido su solicitud. Nos comunicaremos con usted pronto.';
              modal.classList.add('modal--open');
            }
            form.reset();
          } else {
            alert('Hubo un error al enviar la reservación. Por favor intente más tarde.');
          }
        }).catch(error => {
          alert('Hubo un error de red. Verifique su conexión.');
        }).finally(() => {
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
        });
      }
    });
  }

  // Reservation form validation
  validateForm('reservationForm', [
    { id: 'resName',   errorId: 'resNameError',   required: true },
    { id: 'resPhone',  errorId: 'resPhoneError',  required: true, type: 'tel' },
    { id: 'resEmail',  errorId: 'resEmailError',  type: 'email' },
    { id: 'resGuests', errorId: 'resGuestsError', required: true },
    { id: 'resDate',   errorId: 'resDateError',   required: true, type: 'date' },
  ]);

  // Contact form — simple validation
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('ctName');
      const phone = document.getElementById('ctPhone');
      const message = document.getElementById('ctMessage');
      
      let valid = true;
      [name, phone, message].forEach(input => {
        if (input && !input.value.trim()) {
          input.classList.add('error');
          valid = false;
        } else if (input) {
          input.classList.remove('error');
        }
      });

      if (valid) {
        const submitBtn = contactForm.querySelector('.form__submit');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Enviando...';
        submitBtn.disabled = true;

        const formData = new FormData(contactForm);
        const data = Object.fromEntries(formData);

        fetch('/api/contacts', {
          method: 'POST',
          body: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        }).then(response => {
          if (response.ok) {
            const modal = document.getElementById('successModal');
            if (modal) {
              modal.querySelector('.modal__title').textContent = '¡Mensaje Enviado!';
              modal.querySelector('.modal__text').textContent = 'Hemos recibido su mensaje. Nos comunicaremos con usted pronto.';
              modal.classList.add('modal--open');
            }
            contactForm.reset();
          } else {
            alert('Hubo un error al enviar el mensaje. Por favor intente más tarde.');
          }
        }).catch(error => {
          alert('Hubo un error de red. Verifique su conexión.');
        }).finally(() => {
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
        });
      }
    });
  }

  /* ── 9. SCROLL ANIMATIONS (IntersectionObserver) ── */
  const animateElements = document.querySelectorAll('.animate-on-scroll');
  const animateObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-on-scroll--visible');
        animateObserver.unobserve(entry.target); // Only animate once
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

  animateElements.forEach(el => animateObserver.observe(el));

  /* ── 10. BACK TO TOP ── */
  const backToTop = document.getElementById('backToTop');
  if (backToTop) {
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ── 11. SET MIN DATE on reservation form ── */
  const dateInput = document.getElementById('resDate');
  if (dateInput) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', today);
  }

  /* ── 12. CLOSE MODAL on outside click ── */
  const modal = document.getElementById('successModal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.classList.remove('modal--open');
    });
  }

  /* ── 13. Remove input error on focus ── */
  document.querySelectorAll('.form__input, .form__select, .form__textarea').forEach(input => {
    input.addEventListener('focus', () => {
      input.classList.remove('error');
      const errorEl = input.parentElement.querySelector('.form__error');
      if (errorEl) errorEl.classList.remove('show');
    });
  });

  console.log('🔥 Asadero Los Tronquitos — Sitio web cargado correctamente');
});
