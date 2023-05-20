let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.kidsnavbar');

menu.onclick = () => {
    menu.classList.toggle('fa-xmark');
    navbar.classList.toggle('open');
}