const Hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

document.addEventListener('DOMContentLoaded', function() {
    const Hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    Hamburger.addEventListener('click', () => {
        Hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
        Hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    }));
});