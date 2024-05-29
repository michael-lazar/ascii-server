document.addEventListener('DOMContentLoaded', function() {
    const langEn = document.getElementById('lang-en');
    const langZh = document.getElementById('lang-zh');

    const fontDisplay = document.getElementById('font-size-display');
    const fontIncrease = document.getElementById('font-increase');
    const fontDecrease = document.getElementById('font-decrease');

    const whitespaceToggle = document.getElementById('whitespace-toggle');

    const contentEn = document.querySelectorAll('.content-en');
    const contentZh = document.querySelectorAll('.content-zh');

    const bbsDocuments = document.querySelectorAll('.bbs-document');
    const bbsMenuItems = document.querySelectorAll('.bbs-menu > span');

    const toggleToolbarButton = document.getElementById('toggle-toolbar');
    const toolbarElements = document.querySelectorAll('.bbs-controls > div:not(#toggle-toolbar)');

    // Variables
    let bbsFontSize = 20;
    let bbsWrapText = false;
    let isToolbarExpanded = true;
    let bbsLanguage = langZh.classList.contains('active') ? 'zh' : 'en';

    function refreshFontSize() {
        fontDisplay.textContent = `${bbsFontSize}px`;
        document.querySelector('.bbs').style.fontSize = `${bbsFontSize}px`;
    }

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

    fontIncrease.addEventListener("mousedown", function () {
        fontIncrease.classList.add("inverse")
    })
    fontIncrease.addEventListener("mouseup", function () {
        fontIncrease.classList.remove("inverse")
    })
    fontIncrease.addEventListener("mouseleave", function () {
        fontIncrease.classList.remove("inverse")
    })

    fontDecrease.addEventListener("mousedown", function () {
        fontDecrease.classList.add("inverse")
    })
    fontDecrease.addEventListener("mouseup", function () {
        fontDecrease.classList.remove("inverse")
    })
    fontIncrease.addEventListener("mouseleave", function () {
        fontDecrease.classList.remove("inverse")
    })

    toggleToolbarButton.addEventListener('click', function() {
        isToolbarExpanded = !isToolbarExpanded;

        toolbarElements.forEach(element => {
            element.classList.toggle("hidden")
        });

        if (isToolbarExpanded) {
            toggleToolbarButton.textContent = '-';
        } else {
            toggleToolbarButton.textContent = '+';
        }
    });

    whitespaceToggle.addEventListener('click', function() {
        const newWhiteSpace = bbsWrapText ? 'pre' : 'pre-line';

        bbsDocuments.forEach(span => {
            span.style.whiteSpace = newWhiteSpace;
        });

        bbsMenuItems.forEach(span => {
            span.style.whiteSpace = newWhiteSpace;
        });

        whitespaceToggle.classList.toggle('active');
        bbsWrapText = !bbsWrapText;
    });

    fontIncrease.addEventListener('click', function() {
        bbsFontSize += 4;
        refreshFontSize();
    });

    fontDecrease.addEventListener('click', function() {
        bbsFontSize = Math.max(4, bbsFontSize - 4);
        refreshFontSize();
    });

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
