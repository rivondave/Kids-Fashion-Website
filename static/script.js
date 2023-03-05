let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.kidsnavbar');

menu.onclick = () => {
    menu.classList.toggle('fa-xmark');
    navbar.classList.toggle('open');
}




let preveiwContainer = document.querySelector('.products-preview');
let previewBox = preveiwContainer.querySelectorAll('.preview');

document.querySelectorAll('.view').forEach(product =>{
  product.onclick = () =>{
    preveiwContainer.style.display = 'flex';
    let name = product.getAttribute('data-name');
    previewBox.forEach(preview =>{
      let target = preview.getAttribute('data-target');
      if(name == target){
        preview.classList.add('active');
      }
    });
  };
});
previewBox.forEach(close =>{
  close.querySelector('.fa-arrow-right').onclick = () =>{
    close.classList.remove('active');
    preveiwContainer.style.display = 'none';
  };
});