document.addEventListener('DOMContentLoaded', () => {

    // Loader funksiyasi
    const loader = document.querySelector('.loader-wrapper');
    if (loader) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                loader.classList.add('hidden');
            }, 300);
        });
    }

    // --- YANGILANGAN QISM ---
    // Kartalardagi sichqoncha harakatiga mos nur effekti uchun
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--x', `${x}px`);
            card.style.setProperty('--y', `${y}px`);
        });
    });

    // Login sahifasidagi "Kirish" tugmasi uchun simulyatsiya
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.addEventListener('click', (e) => {
            e.preventDefault(); // Sahifani yangilamaslik uchun
            document.body.style.transition = "opacity 0.5s ease";
            document.body.style.opacity = 0;
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 500);
        });
    }

    // Kurs sahifasidagi modullarni ochish/yopish
    document.querySelectorAll('.module-header').forEach(header => {
        header.addEventListener('click', () => {
            if(header.parentElement.classList.contains('locked')) return;
            
            const lessonList = header.nextElementSibling;
            const icon = header.querySelector('i.bx-chevron-down, i.bx-chevron-up');
            if(lessonList && icon) {
                lessonList.classList.toggle('show');
                icon.classList.toggle('bx-chevron-down');
                icon.classList.toggle('bx-chevron-up');
            }
        });
    });
});