document.addEventListener('DOMContentLoaded', function() {
const langEn = document.getElementById('lang-en');
const langZh = document.getElementById('lang-zh');
const textsEn = document.querySelectorAll('.text-en');
const textsZh = document.querySelectorAll('.text-zh');

function showEnglish() {
  textsEn.forEach(el => {
    el.classList.add('visible');
    el.classList.remove('hidden');
  });
  textsZh.forEach(el => {
    el.classList.add('hidden');
    el.classList.remove('visible');
  });
  langEn.classList.add('active');
  langZh.classList.remove('active');
}

function showChinese() {
  textsEn.forEach(el => {
    el.classList.add('hidden');
    el.classList.remove('visible');
  });
  textsZh.forEach(el => {
    el.classList.add('visible');
    el.classList.remove('hidden');
  });
  langZh.classList.add('active');
  langEn.classList.remove('active');
}

langEn.addEventListener('click', showEnglish);
langZh.addEventListener('click', showChinese);
});
