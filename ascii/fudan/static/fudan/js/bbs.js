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

    // Menu navigation state
    let currentMenuIndex = 0;
    let menuLinks = [];
    let isMenuPage = false;

    // Initialize navigation
    function initializeNavigation() {
        const bbsMenu = document.querySelector('.bbs-menu');
        if (bbsMenu) {
            isMenuPage = true;
            menuLinks = Array.from(bbsMenu.querySelectorAll('a'));
            if (menuLinks.length > 0) {
                highlightMenuLink(0);
            }
        }
    }

    // Highlight menu link for accessibility
    function highlightMenuLink(index) {
        menuLinks.forEach((link, i) => {
            if (i === index) {
                link.setAttribute('aria-selected', 'true');
                link.style.backgroundColor = '#333';
                link.style.color = '#fff';
                link.focus();
            } else {
                link.setAttribute('aria-selected', 'false');
                link.style.backgroundColor = '';
                link.style.color = '';
            }
        });
        currentMenuIndex = index;
    }

    // Navigate to parent page
    function navigateToParent() {
        const parentLink = document.querySelector('.bbs-nav a');
        if (parentLink) {
            window.location.href = parentLink.href;
        }
    }

    // Navigate to previous sibling
    function navigateToPrevious() {
        const prevLink = document.querySelector('.bbs-controls a[href]:first-of-type');
        if (prevLink && prevLink.textContent.trim() === '<') {
            window.location.href = prevLink.href;
        }
    }

    // Navigate to next sibling
    function navigateToNext() {
        const nextLink = document.querySelector('.bbs-controls a[href]');
        if (nextLink && nextLink.textContent.trim() === '>') {
            window.location.href = nextLink.href;
        }
    }

    // Keyboard navigation
    document.addEventListener('keydown', function(event) {
        // Toggle language with 't'
        if (event.key === 't') {
            toggleLanguage();
            event.preventDefault();
            return;
        }

        // Handle arrow keys
        switch(event.key) {
            case 'ArrowUp':
                if (isMenuPage) {
                    // Menu page: move cursor up
                    if (currentMenuIndex > 0) {
                        highlightMenuLink(currentMenuIndex - 1);
                    }
                } else {
                    // Document page: navigate to previous sibling
                    navigateToPrevious();
                }
                event.preventDefault();
                break;

            case 'ArrowDown':
                if (isMenuPage) {
                    // Menu page: move cursor down
                    if (currentMenuIndex < menuLinks.length - 1) {
                        highlightMenuLink(currentMenuIndex + 1);
                    }
                } else {
                    // Document page: navigate to next sibling
                    navigateToNext();
                }
                event.preventDefault();
                break;

            case 'ArrowLeft':
                // Both pages: navigate to parent
                navigateToParent();
                event.preventDefault();
                break;

            case 'ArrowRight':
                if (isMenuPage && menuLinks.length > 0) {
                    // Menu page: open selected link
                    window.location.href = menuLinks[currentMenuIndex].href;
                }
                event.preventDefault();
                break;
        }
    });

    // Initialize navigation when page loads
    initializeNavigation();
});
