//console.log('test');
// Modal open & close
const openButton = document.getElementsByClassName('DPimg');
//const modal = document.querySelector('.modal');
const modal = document.getElementById('modal-container');
const overlay = modal.querySelector('.modal_overlay');
const closeBtn = modal.querySelector('.close_btn');

/*
const openModal = () => {
  modal.classList.remove('hidden');
};
const closeModal = () => {
  modal.classList.add('hidden');
};*/

//overlay.addEventListener('click', closeModal);
closeBtn.addEventListener('click', function (e) {
  modal.classList.toggle('opaque');
  document
    .getElementById('player')
    .contentWindow.postMessage(
      '{"event":"command", "func":"stopVideo", "args":""}',
      '*'
    ); // iframe 영상 멈추기
  modal.addEventListener('transitionend', function (e) {
    this.classList.toggle('unstaged');
    this.removeEventListener('transitionend', arguments.callee);
  });
});

overlay.addEventListener('click', function (e) {
  modal.classList.toggle('opaque');
  document
    .getElementById('player')
    .contentWindow.postMessage(
      '{"event":"command", "func":"stopVideo", "args":""}',
      '*'
    ); // iframe 영상 멈추기
  modal.addEventListener('transitionend', function (e) {
    this.classList.toggle('unstaged');
    this.removeEventListener('transitionend', arguments.callee);
  });
});

for (let i = 0; i < openButton.length; i++) {
  openButton[i].addEventListener('click', function (e) {
    modal.classList.toggle('opaque');
    modal.classList.toggle('unstaged');
  });
}

// Youatube Video
//document.getElementById("player").contentWindow.postMessage('{"event":"command", "func":"stopVideo", "args":""}', '*');

function goodBtnToggle() {
  let goodBtn = document.querySelector('.good-btn');
  let badBtn = document.querySelector('.bad-btn');
  if (badBtn.classList.contains('active')) {
    badBtn.classList.toggle('active');
  }
  goodBtn.classList.toggle('active');
}
function badBtnToggle() {
  let goodBtn = document.querySelector('.good-btn');
  let badBtn = document.querySelector('.bad-btn');
  if (goodBtn.classList.contains('active')) {
    goodBtn.classList.toggle('active');
  }
  badBtn.classList.toggle('active');
}
