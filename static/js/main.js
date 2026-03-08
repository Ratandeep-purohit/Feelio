/**
 * Feelio v2.0 — Main JavaScript Module
 * Handles: sidebar, flash toasts, scroll-to-top, fade-up animations,
 *          password toggle, mobile responsiveness.
 */

document.addEventListener('DOMContentLoaded', () => {

    // ── Flash Toast Auto-Dismiss ────────────────────────────────────
    document.querySelectorAll('.flash-toast').forEach(toast => {
        setTimeout(() => dismissToast(toast), 5000);
    });
    function dismissToast(toast) {
        toast.style.transition = 'all 0.4s ease';
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(60px)';
        setTimeout(() => toast.remove(), 400);
    }

    // ── Sidebar Mobile Toggle ───────────────────────────────────────
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
        // Close sidebar on outside click
        document.addEventListener('click', (e) => {
            if (sidebar.classList.contains('open') &&
                !sidebar.contains(e.target) &&
                !menuToggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        });
    }

    // ── Scroll to Top Button ────────────────────────────────────────
    const scrollTopBtn = document.getElementById('scrollTop');
    if (scrollTopBtn) {
        window.addEventListener('scroll', () => {
            scrollTopBtn.classList.toggle('visible', window.scrollY > 300);
        });
        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ── Intersection Observer – Fade Up Animations ──────────────────
    const fadeEls = document.querySelectorAll('.fade-up');
    if ('IntersectionObserver' in window && fadeEls.length) {
        const io = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in');
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
        fadeEls.forEach(el => io.observe(el));
    } else {
        // Fallback: show all immediately
        fadeEls.forEach(el => el.classList.add('in'));
    }

    // ── Password Toggle ─────────────────────────────────────────────
    window.togglePass = function (inputId, btn) {
        const input = document.getElementById(inputId);
        if (!input) return;
        const isText = input.type === 'text';
        input.type = isText ? 'password' : 'text';
        btn.querySelector('i').className = isText ? 'fa-solid fa-eye' : 'fa-solid fa-eye-slash';
    };

    // ── Active Nav Link Highlight (fallback for dynamic pages) ──────
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-item').forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.startsWith(href) && href !== '/') {
            link.classList.add('active');
        }
    });

    // ── Risk Meter Bar Animations (trigger on load) ─────────────────
    document.querySelectorAll('.risk-meter-fill').forEach(bar => {
        const target = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => { bar.style.width = target; }, 200);
    });

    // ── Progress Bar Animations ─────────────────────────────────────
    document.querySelectorAll('.progress-fill').forEach(bar => {
        const target = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => { bar.style.width = target; }, 300);
    });

    // ── Score Ring Animation ─────────────────────────────────────────
    document.querySelectorAll('.ring-fill').forEach(circle => {
        const dashArray = circle.getAttribute('stroke-dasharray');
        if (dashArray) {
            const targetDash = dashArray.split(' ')[0];
            circle.setAttribute('stroke-dasharray', `0 251.3`);
            setTimeout(() => {
                circle.style.transition = 'stroke-dasharray 1.5s cubic-bezier(.4,0,.2,1)';
                circle.setAttribute('stroke-dasharray', `${targetDash} 251.3`);
            }, 400);
        }
    });

    // ── Keyboard Shortcut: Alt+C → Check-In ─────────────────────────
    document.addEventListener('keydown', (e) => {
        if (e.altKey && e.key === 'c') {
            const link = document.querySelector('[href*="checkin"]');
            if (link) window.location.href = link.href;
        }
    });

    // ── Tooltip on hover (title attr) ───────────────────────────────
    document.querySelectorAll('[title]').forEach(el => {
        el.addEventListener('mouseenter', () => {
            // Native tooltips are fine; just ensure they have pointer cursor
            if (!el.style.cursor) el.style.cursor = 'default';
        });
    });

    console.log('%c🧠 Feelio v2.0 loaded successfully!', 'color:#6c3bef;font-weight:700;font-size:14px');
});
