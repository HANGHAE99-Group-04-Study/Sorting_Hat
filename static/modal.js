// Modal open & close
const openButton = document.getElementsByClassName('screen'); // 오픈 할 객체 찾아서 배열로 저장
const modal = document.getElementById('modal-container'); // 이벤트를 넣을 상세 페이지 부분 지정
const overlay = modal.querySelector('.modal_overlay'); // 상세 페이지 배경 부분 지정
const closeBtn = modal.querySelector('.close_btn'); // 상세 페이지 내 버튼 부분 지정

// 닫기 버튼 클릭 시 상세페이지 닫도록 이벤트 추가
closeBtn.addEventListener('click', function (e) {
  modal.classList.toggle('opaque');
  modal.addEventListener('transitionend', function (e) {
    this.classList.toggle('unstaged');
    this.removeEventListener('transitionend', arguments.callee);
  });
});

// 상세페이지에서 배경 클릭 시 상세페이지 닫도록 이벤트 추가
overlay.addEventListener('click', function (e) {
  modal.classList.toggle('opaque');
  modal.addEventListener('transitionend', function (e) {
    this.classList.toggle('unstaged');
    this.removeEventListener('transitionend', arguments.callee);
  });
});

// screen 클래스 부분 클릭 시 상세페이지 나오도록 이벤트 추가
window.addEventListener("load", function(event) {
  for (let i = 0; i < openButton.length; i++) {
    openButton[i].addEventListener('click', function (e) {
      modal.classList.toggle('opaque');
      modal.classList.toggle('unstaged');
    });
  }
})