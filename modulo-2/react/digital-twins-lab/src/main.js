import './input.css';
import 'flowbite';
import headerHtml from '../components/Header.html?raw';
import formHtml from '../components/FormBookingDemo.html?raw';
import footerHtml from '../components/Footer.html?raw';

/**
 * Inserta fragmentos HTML estáticos de forma segura (OWASP):
 * - Sin innerHTML sobre el documento principal
 * - Sin eval ni inserción de contenido dinámico del usuario
 * - DOMParser + replaceChildren para nodos confiables del mismo origen
 */
function mountComponent(html, targetId) {
  const target = document.getElementById(targetId);
  if (!target) return;

  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');
  target.replaceChildren(...doc.body.children);
}

function initFooterYear() {
  const yearEl = document.getElementById('footer-year');
  if (yearEl) {
    yearEl.textContent = String(new Date().getFullYear());
  }
}

function initBookingForm() {
  const form = document.getElementById('booking-demo-form');
  if (!form) return;

  form.addEventListener('submit', (event) => {
    event.preventDefault();

    const submitButton = form.querySelector('[type="submit"]');
    if (!submitButton) return;

    submitButton.textContent = 'Solicitud enviada';
    submitButton.disabled = true;
  });
}

mountComponent(headerHtml, 'header-root');
mountComponent(formHtml, 'form-root');
mountComponent(footerHtml, 'footer-root');
initFooterYear();
initBookingForm();
