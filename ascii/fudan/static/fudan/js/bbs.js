document.addEventListener('DOMContentLoaded', function() {
    const langEn = document.getElementById('lang-en');
    const langZh = document.getElementById('lang-zh');
    const textsEn = document.querySelectorAll('.text-en');
    const textsZh = document.querySelectorAll('.text-zh');
    let currentLanguage = 'en'; // Default language

    function updateUrlParameter(lang) {
        let currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('lang', lang);
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
        currentLanguage = 'en';
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
        currentLanguage = 'zh-cn';
    }

    function toggleLanguage() {
        if (currentLanguage === 'en') {
            showChinese();
        } else {
            showEnglish();
        }
    }

    langEn.addEventListener('click', showEnglish);
    langZh.addEventListener('click', showChinese);

    // Bind the 't' key to toggle languages
    document.addEventListener('keydown', function(event) {
        if (event.key === 't') {
            toggleLanguage();
            event.preventDefault(); // Prevent any default behavior triggered by 't'
        }
    });
});
