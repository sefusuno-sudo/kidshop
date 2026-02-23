/**
 * KidsShop – JavaScript principal
 */

document.addEventListener('DOMContentLoaded', function () {

  // ── Auto-dismiss flash messages after 5s ──────────────────────────
  setTimeout(function () {
    document.querySelectorAll('.alert.alert-dismissible').forEach(function (el) {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
      bsAlert.close();
    });
  }, 5000);

  // ── Navbar scroll effect ──────────────────────────────────────────
  const navbar = document.getElementById('mainNav');
  if (navbar) {
    window.addEventListener('scroll', function () {
      navbar.classList.toggle('shadow', window.scrollY > 30);
    });
  }

  // ── Smooth scroll for anchor links ───────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Quantity helpers (global) ─────────────────────────────────────
  window.changeQty = function (delta) {
    const inp = document.getElementById('qty');
    if (inp) inp.value = Math.max(1, parseInt(inp.value || 1) + delta);
  };

  window.changeQtyForm = function (btn, delta) {
    const form = btn.closest('form');
    const inp  = form.querySelector('input[name="quantity"]');
    if (inp) {
      inp.value = Math.max(0, parseInt(inp.value || 1) + delta);
      form.submit();
    }
  };

  // ── Image switcher for product detail ────────────────────────────
  window.switchImage = function (el) {
    const main = document.getElementById('mainImage');
    if (main) main.src = el.src;
    document.querySelectorAll('.img-thumb').forEach(t => t.classList.remove('active'));
    el.classList.add('active');
  };

  // ── Product cards hover effect enhancement ────────────────────────
  document.querySelectorAll('.product-card').forEach(function (card) {
    card.addEventListener('mouseenter', function () {
      this.style.transition = 'transform .3s, box-shadow .3s';
    });
  });

  // ── Toast notification helper ─────────────────────────────────────
  window.showToast = function (message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed bottom-0 end-0 m-3 rounded-3 shadow`;
    toast.style.cssText = 'z-index:9999; min-width:250px; animation:fadeIn .3s';
    toast.innerHTML = `${message}<button type="button" class="btn-close float-end" onclick="this.parentElement.remove()"></button>`;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3500);
  };
});
