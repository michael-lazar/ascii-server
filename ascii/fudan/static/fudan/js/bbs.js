document.addEventListener('DOMContentLoaded', function() {
    const langEn = document.getElementById('lang-en');
    const langZh = document.getElementById('lang-zh');
    const textsEn = document.querySelectorAll('.text-en');
    const textsZh = document.querySelectorAll('.text-zh');

    function updateUrlParameter(lang) {
        // Get the current URL
        let currentUrl = new URL(window.location.href);
        // Set or replace the 'lang' query parameter
        currentUrl.searchParams.set('lang', lang);
        // Update the URL without creating a new history entry
        window.history.replaceState({ path: currentUrl.href }, '', currentUrl.href);
    }

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
        updateUrlParameter('en');
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
        updateUrlParameter('zh-cn');
    }

    langEn.addEventListener('click', showEnglish);
    langZh.addEventListener('click', showChinese);
});
