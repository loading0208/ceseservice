const container = document.getElementById('imagecontainer');
const imgs = document.querySelectorAll('#imagecontainer img');

const backbtn = document.getElementById('back')
const nextbtn = document.getElementById('next')

//สร้างตัวนับภาพ
let idx = 0;
let interval = setInterval(slide, 2000);

function slide() {
  idx++;
  changeImage();
}

function changeImage() {
  if (idx > imgs.length - 1) {
    idx = 0;
  } else if (idx < 0) {
    idx = imgs.length - 1;
  }
  container.style.transform = `translateX(${-idx*500}px)`;
}

backbtn.addEventListener('click', () => {
  idx--;
  changeImage();
  resetInterval();
});

nextbtn.addEventListener('click', () => {
  idx++;
  changeImage();
  resetInterval();
});

function resetInterval() {
  clearInterval(interval);
  interval = setInterval(slide, 2000);
}
