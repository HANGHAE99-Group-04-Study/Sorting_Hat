// Modal open & close
const openButton = document.getElementsByClassName('screen');
const modal = document.getElementById('modal-container');
const overlay = modal.querySelector('.modal_overlay');
const closeBtn = modal.querySelector('.close_btn');


closeBtn.addEventListener('click', function (e) {
  modal.classList.toggle('opaque');

  modal.addEventListener('transitionend', function (e) {
    this.classList.toggle('unstaged');
    this.removeEventListener('transitionend', arguments.callee);
  });
});

overlay.addEventListener('click', function (e) {
  modal.classList.toggle('opaque');

  modal.addEventListener('transitionend', function (e) {
    this.classList.toggle('unstaged');
    this.removeEventListener('transitionend', arguments.callee);
  });
});

window.addEventListener("load", function(event) {
  for (let i = 0; i < openButton.length; i++) {
    openButton[i].addEventListener('click', function (e) {
      modal.classList.toggle('opaque');
      modal.classList.toggle('unstaged');
    });
  }
})