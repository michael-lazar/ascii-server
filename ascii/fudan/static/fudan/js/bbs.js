document.addEventListener('DOMContentLoaded', function() {
    const langEn = document.getElementById('lang-en');
    const langZh = document.getElementById('lang-zh');

    const fontIncrease = document.getElementById('font-increase');
    const fontDecrease = document.getElementById('font-decrease');

    const whitespaceToggle = document.getElementById('whitespace-toggle');

    const contentEn = document.querySelectorAll('.content-en');
    const contentZh = document.querySelectorAll('.content-zh');

    const bbs = document.querySelector('.bbs')
    const bbsDocument = document.querySelector('.bbs-document');
    const bbsMenuItems = document.querySelectorAll('.bbs-menu > span');

    let bbsLanguage = langZh.classList.contains('active') ? 'zh' : 'en';
    let bbsFontSize = 2.38; // Initial font size in vw units
    let bbsWrapText = false; // Initial text wrapping

    whitespaceToggle.addEventListener('click', function() {
        const newWhiteSpace = bbsWrapText ? 'pre' : 'pre-line';

        if (bbsDocument) {
            bbsDocument.style.whiteSpace = newWhiteSpace;
        }

        bbsMenuItems.forEach(span => {
            span.style.whiteSpace = newWhiteSpace;
        });

        whitespaceToggle.classList.toggle('active');
        bbsWrapText = !bbsWrapText;
    });


    fontIncrease.addEventListener('click', function() {
        bbsFontSize += 0.2;
        bbs.style.fontSize = `${bbsFontSize}vw`;
    });

    fontDecrease.addEventListener('click', function() {
        bbsFontSize -= 0.2;
        if (bbsFontSize < 1) bbsFontSize = 1; // Minimum font size limit
        bbs.style.fontSize = `${bbsFontSize}vw`;
    });

    function showEnglish() {
        contentEn.forEach(el => {
            el.classList.remove('hidden');
        });
        contentZh.forEach(el => {
            el.classList.add('hidden');
        });
        langEn.classList.add('active');
        langZh.classList.remove('active');

        bbsLanguage = 'en';
    }

    function showChinese() {
        contentEn.forEach(el => {
            el.classList.add('hidden');
        });
        contentZh.forEach(el => {
            el.classList.remove('hidden');
        });
        langZh.classList.add('active');
        langEn.classList.remove('active');

        bbsLanguage = 'zh-cn';
    }

    function toggleLanguage() {
        if (bbsLanguage === 'en') {
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
