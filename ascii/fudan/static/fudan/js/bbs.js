document.addEventListener("DOMContentLoaded", function () {
  const langEn = document.getElementById("lang-en");
  const langZh = document.getElementById("lang-zh");

  const fontDisplay = document.getElementById("font-size-display");
  const fontIncrease = document.getElementById("font-increase");
  const fontDecrease = document.getElementById("font-decrease");

  const whitespaceToggle = document.getElementById("whitespace-toggle");

  const contentEn = document.querySelectorAll(".content-en");
  const contentZh = document.querySelectorAll(".content-zh");

  const bbsDocuments = document.querySelectorAll(".bbs-document");
  const bbsMenuItems = document.querySelectorAll(".bbs-menu > span");

  const toggleToolbarButton = document.getElementById("toggle-toolbar");
  const toolbarElements = document.querySelectorAll(
    ".bbs-controls > div:not(#toggle-toolbar)",
  );

  // Variables
  let bbsFontSize = 20;
  let bbsWrapText = false;
  let isToolbarExpanded = true;
  let bbsLanguage = langZh.classList.contains("active") ? "zh" : "en";

  function refreshFontSize() {
    fontDisplay.textContent = `${bbsFontSize}px`;
    document.querySelector(".bbs").style.fontSize = `${bbsFontSize}px`;
  }

  function showEnglish() {
    contentEn.forEach((el) => {
      el.classList.remove("hidden");
    });
    contentZh.forEach((el) => {
      el.classList.add("hidden");
    });
    langEn.classList.add("active");
    langZh.classList.remove("active");

    bbsLanguage = "en";
  }

  function showChinese() {
    contentEn.forEach((el) => {
      el.classList.add("hidden");
    });
    contentZh.forEach((el) => {
      el.classList.remove("hidden");
    });
    langZh.classList.add("active");
    langEn.classList.remove("active");

    bbsLanguage = "zh-cn";
  }

  function toggleLanguage() {
    if (bbsLanguage === "en") {
      showChinese();
    } else {
      showEnglish();
    }
  }

  fontIncrease.addEventListener("mousedown", function () {
    fontIncrease.classList.add("inverse");
  });
  fontIncrease.addEventListener("mouseup", function () {
    fontIncrease.classList.remove("inverse");
  });
  fontIncrease.addEventListener("mouseleave", function () {
    fontIncrease.classList.remove("inverse");
  });

  fontDecrease.addEventListener("mousedown", function () {
    fontDecrease.classList.add("inverse");
  });
  fontDecrease.addEventListener("mouseup", function () {
    fontDecrease.classList.remove("inverse");
  });
  fontIncrease.addEventListener("mouseleave", function () {
    fontDecrease.classList.remove("inverse");
  });

  toggleToolbarButton.addEventListener("click", function () {
    isToolbarExpanded = !isToolbarExpanded;

    toolbarElements.forEach((element) => {
      element.classList.toggle("hidden");
    });

    if (isToolbarExpanded) {
      toggleToolbarButton.textContent = "-";
    } else {
      toggleToolbarButton.textContent = "+";
    }
  });

  whitespaceToggle.addEventListener("click", function () {
    const newWhiteSpace = bbsWrapText ? "pre" : "pre-line";

    bbsDocuments.forEach((span) => {
      span.style.whiteSpace = newWhiteSpace;
    });

    bbsMenuItems.forEach((span) => {
      span.style.whiteSpace = newWhiteSpace;
    });

    whitespaceToggle.classList.toggle("active");
    bbsWrapText = !bbsWrapText;
  });

  fontIncrease.addEventListener("click", function () {
    bbsFontSize += 4;
    refreshFontSize();
  });

  fontDecrease.addEventListener("click", function () {
    bbsFontSize = Math.max(4, bbsFontSize - 4);
    refreshFontSize();
  });

  langEn.addEventListener("click", showEnglish);
  langZh.addEventListener("click", showChinese);

  // Menu navigation state
  let currentMenuIndex = 0;
  let menuLinksZh = [];
  let menuLinksEn = [];
  let isMenuPage = false;

  // Initialize navigation
  function initializeNavigation() {
    const bbsMenus = document.querySelectorAll(".bbs-menu");
    if (bbsMenus.length > 0) {
      isMenuPage = true;
      // Get links from both language menus
      const zhMenu = document.querySelector(".bbs-menu.content-zh");
      const enMenu = document.querySelector(".bbs-menu.content-en");

      if (zhMenu) {
        menuLinksZh = Array.from(zhMenu.querySelectorAll("a"));
      }
      if (enMenu) {
        menuLinksEn = Array.from(enMenu.querySelectorAll("a"));
      }

      if (menuLinksZh.length > 0 || menuLinksEn.length > 0) {
        restoreMenuPosition();
      }
    }
  }

  // Save current menu position to session storage
  function saveMenuPosition() {
    if (isMenuPage) {
      const menuKey = `fudan_menu_${window.location.pathname}`;
      sessionStorage.setItem(menuKey, currentMenuIndex.toString());
    }
  }

  // Restore menu position from session storage or find current page
  function restoreMenuPosition() {
    const menuKey = `fudan_menu_${window.location.pathname}`;
    let targetIndex = 0;

    // First try to find the link that matches the referring page
    const referrer = document.referrer;
    if (referrer) {
      const referrerPath = new URL(referrer).pathname;

      // Check both language menus for matching link
      const allLinks = [...menuLinksZh, ...menuLinksEn];
      const matchingLinkIndex = allLinks.findIndex(link => {
        const linkPath = new URL(link.href).pathname;
        return linkPath === referrerPath;
      });

      if (matchingLinkIndex !== -1) {
        // Convert to menu index (links are duplicated in both languages)
        targetIndex = matchingLinkIndex % Math.max(menuLinksZh.length, menuLinksEn.length);
      }
    }

    // If no referrer match, try session storage
    if (targetIndex === 0) {
      const savedIndex = sessionStorage.getItem(menuKey);
      if (savedIndex !== null) {
        targetIndex = parseInt(savedIndex, 10);
      }
    }

    // Ensure index is within bounds
    const maxLinks = Math.max(menuLinksZh.length, menuLinksEn.length);
    targetIndex = Math.max(0, Math.min(targetIndex, maxLinks - 1));

    highlightMenuLink(targetIndex);
  }

  // Highlight menu link for accessibility
  function highlightMenuLink(index) {
    // Update both Chinese and English menus
    [menuLinksZh, menuLinksEn].forEach((linkArray) => {
      linkArray.forEach((link, i) => {
        if (i === index) {
          link.setAttribute("aria-selected", "true");
          link.classList.add("keyboard-selected");
          // Only focus the visible link
          if (
            !link
              .closest(".content-zh, .content-en")
              .classList.contains("hidden")
          ) {
            link.focus();
          }
        } else {
          link.setAttribute("aria-selected", "false");
          link.classList.remove("keyboard-selected");
        }
      });
    });
    currentMenuIndex = index;
    // Save position whenever it changes
    saveMenuPosition();
  }

  // Navigate to parent page
  function navigateToParent() {
    const parentLink = document.querySelector(".bbs-nav a");
    if (parentLink) {
      window.location.href = parentLink.href;
    }
  }

  // Navigate to previous sibling
  function navigateToPrevious() {
    const prevLink = document.querySelector(
      ".bbs-controls a[href]:first-of-type",
    );
    if (prevLink && prevLink.textContent.trim() === "<") {
      window.location.href = prevLink.href;
    }
  }

  // Navigate to next sibling
  function navigateToNext() {
    const nextLink = document.querySelector(".bbs-controls a[href]");
    if (nextLink && nextLink.textContent.trim() === ">") {
      window.location.href = nextLink.href;
    }
  }

  // Keyboard navigation
  document.addEventListener("keydown", function (event) {
    // Toggle language with 't'
    if (event.key === "t") {
      toggleLanguage();
      event.preventDefault();
      return;
    }

    // Handle arrow keys
    switch (event.key) {
      case "ArrowUp":
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

      case "ArrowDown":
        if (isMenuPage) {
          // Menu page: move cursor down
          const maxLinks = Math.max(menuLinksZh.length, menuLinksEn.length);
          if (currentMenuIndex < maxLinks - 1) {
            highlightMenuLink(currentMenuIndex + 1);
          }
        } else {
          // Document page: navigate to next sibling
          navigateToNext();
        }
        event.preventDefault();
        break;

      case "ArrowLeft":
        // Both pages: navigate to parent
        navigateToParent();
        event.preventDefault();
        break;

      case "ArrowRight":
        if (isMenuPage) {
          // Menu page: open selected link from currently visible menu
          const currentLinks = bbsLanguage === "en" ? menuLinksEn : menuLinksZh;
          if (
            currentLinks.length > 0 &&
            currentMenuIndex < currentLinks.length
          ) {
            window.location.href = currentLinks[currentMenuIndex].href;
          }
        }
        event.preventDefault();
        break;
    }
  });

  // Initialize navigation when page loads
  initializeNavigation();
});
