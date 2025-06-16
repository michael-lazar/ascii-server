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

  // Load saved settings immediately to prevent flashing
  let bbsFontSize = parseInt(sessionStorage.getItem("fudan_font_size")) || 20;
  let bbsWrapText = sessionStorage.getItem("fudan_wrap_text") === "true";
  let isToolbarExpanded =
    sessionStorage.getItem("fudan_toolbar_expanded") !== "true"; // default false
  let bbsLanguage = langZh.classList.contains("active") ? "zh" : "en";

  // Apply settings immediately to prevent flashing
  function applySettingsImmediately() {
    // Apply font size
    if (bbsFontSize !== 20) {
      document.querySelector(".bbs").style.fontSize = `${bbsFontSize}px`;
    }

    // Apply wrap setting
    if (bbsWrapText) {
      const newWhiteSpace = "pre-line";
      document.querySelectorAll(".bbs-document").forEach((span) => {
        span.style.whiteSpace = newWhiteSpace;
      });
      document.querySelectorAll(".bbs-menu > span").forEach((span) => {
        span.style.whiteSpace = newWhiteSpace;
      });
    }

    // Apply toolbar collapsed state
    if (!isToolbarExpanded) {
      const collapsibleElements = document.querySelectorAll(
        ".control.collapsible",
      );
      collapsibleElements.forEach((element) => {
        element.classList.add("hidden");
      });
    }
  }

  // Apply settings as soon as possible
  applySettingsImmediately();

  function refreshFontSize() {
    fontDisplay.textContent = `${bbsFontSize}px`;
    document.querySelector(".bbs").style.fontSize = `${bbsFontSize}px`;
    // Save font size to session storage
    sessionStorage.setItem("fudan_font_size", bbsFontSize.toString());
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

    const collapsibleElements = document.querySelectorAll(
      ".control.collapsible",
    );
    collapsibleElements.forEach((element) => {
      element.classList.toggle("hidden");
    });

    if (isToolbarExpanded) {
      toggleToolbarButton.textContent = "-";
    } else {
      toggleToolbarButton.textContent = "+";
    }

    // Save toolbar state to session storage
    sessionStorage.setItem(
      "fudan_toolbar_expanded",
      isToolbarExpanded.toString(),
    );
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

    // Save wrap text state to session storage
    sessionStorage.setItem("fudan_wrap_text", bbsWrapText.toString());
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

  // Initialize UI to reflect saved state
  function initializeUIState() {
    // Update font size display
    fontDisplay.textContent = `${bbsFontSize}px`;

    // Update wrap toggle state
    if (bbsWrapText) {
      whitespaceToggle.classList.add("active");
    }

    // Update toolbar toggle button
    if (!isToolbarExpanded) {
      toggleToolbarButton.textContent = "+";
    }
  }

  // Initialize UI state
  initializeUIState();

  // Navigation state
  let currentLinkIndex = 0;
  let allLinksZh = [];
  let allLinksEn = [];
  let parentLinks = [];
  let isMenuPage = false;
  let hasNavigation = false;

  // Initialize navigation
  function initializeNavigation() {
    const bbsContent = document.querySelector(".bbs-content");
    if (bbsContent) {
      hasNavigation = true;

      // Check if this is a menu page
      isMenuPage = bbsContent.querySelector(".bbs-menu") !== null;

      // Get parent links (always present)
      parentLinks = Array.from(bbsContent.querySelectorAll(".bbs-nav a"));

      // Get all links from Chinese content
      const zhContent = bbsContent.querySelector(".content-zh");
      if (zhContent) {
        const zhMenuLinks = Array.from(
          zhContent.querySelectorAll(".bbs-menu a"),
        );
        allLinksZh = [...parentLinks, ...zhMenuLinks];
      } else {
        allLinksZh = [...parentLinks];
      }

      // Get all links from English content
      const enContent = bbsContent.querySelector(".content-en");
      if (enContent) {
        const enMenuLinks = Array.from(
          enContent.querySelectorAll(".bbs-menu a"),
        );
        allLinksEn = [...parentLinks, ...enMenuLinks];
      } else {
        allLinksEn = [...parentLinks];
      }

      if (allLinksZh.length > 0 || allLinksEn.length > 0) {
        restoreNavigationPosition();
      }
    }
  }

  // Save current navigation position to session storage
  function saveNavigationPosition() {
    if (hasNavigation) {
      const navKey = `fudan_nav_${window.location.pathname}`;
      sessionStorage.setItem(navKey, currentLinkIndex.toString());
    }
  }

  // Restore navigation position from session storage or find current page
  function restoreNavigationPosition() {
    const navKey = `fudan_nav_${window.location.pathname}`;
    let targetIndex = 0;
    let isNavigatingBack = false;

    // Check if we're navigating back from a child page
    const referrer = document.referrer;
    if (referrer) {
      const referrerPath = new URL(referrer).pathname;

      // Check if referrer matches any of our links (navigating back from child)
      const allLinks = [...allLinksZh, ...allLinksEn];
      const matchingLinkIndex = allLinks.findIndex((link) => {
        const linkPath = new URL(link.href).pathname;
        return linkPath === referrerPath;
      });

      if (matchingLinkIndex !== -1) {
        // We're navigating back - restore cursor to the link we came from
        isNavigatingBack = true;
        targetIndex =
          matchingLinkIndex % Math.max(allLinksZh.length, allLinksEn.length);
      } else {
        // Check if current page is a child of the referrer (navigating forward)
        // Look for referrer in our parent links
        const isNavigatingForward = parentLinks.some((link) => {
          const linkPath = new URL(link.href).pathname;
          return linkPath === referrerPath;
        });

        if (isNavigatingForward) {
          // Navigating forward to child - reset to first menu item
          targetIndex = isMenuPage && parentLinks.length > 0 ? parentLinks.length : 0;
        }
      }
    }

    // If not navigating back and no forward navigation detected, try session storage
    if (!isNavigatingBack && targetIndex === 0) {
      const savedIndex = sessionStorage.getItem(navKey);
      if (savedIndex !== null) {
        targetIndex = parseInt(savedIndex, 10);
      }
    }

    // Default to first menu item if we have parent links and no other positioning
    if (targetIndex === 0 && isMenuPage && parentLinks.length > 0) {
      targetIndex = parentLinks.length; // Start at first menu item
    }

    // Ensure index is within bounds
    const maxLinks = Math.max(allLinksZh.length, allLinksEn.length);
    targetIndex = Math.max(0, Math.min(targetIndex, maxLinks - 1));

    highlightNavigationLink(targetIndex);
  }

  // Highlight navigation link for accessibility
  function highlightNavigationLink(index) {
    // Update all links (parent + menu/content links)
    [allLinksZh, allLinksEn].forEach((linkArray) => {
      linkArray.forEach((link, i) => {
        if (i === index) {
          link.setAttribute("aria-selected", "true");
          link.classList.add("keyboard-selected");
          // Only focus if link is visible (not in hidden language content)
          const parentContent = link.closest(".content-zh, .content-en");
          if (!parentContent || !parentContent.classList.contains("hidden")) {
            link.focus();
          }
        } else {
          link.setAttribute("aria-selected", "false");
          link.classList.remove("keyboard-selected");
        }
      });
    });
    currentLinkIndex = index;
    // Save position whenever it changes
    saveNavigationPosition();
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
        if (hasNavigation) {
          // Move cursor up through all links (parent + menu/content)
          if (currentLinkIndex > 0) {
            highlightNavigationLink(currentLinkIndex - 1);
          }
        } else {
          // Fallback: navigate to previous sibling
          navigateToPrevious();
        }
        event.preventDefault();
        break;

      case "ArrowDown":
        if (hasNavigation) {
          // Move cursor down through all links (parent + menu/content)
          const maxLinks = Math.max(allLinksZh.length, allLinksEn.length);
          if (currentLinkIndex < maxLinks - 1) {
            highlightNavigationLink(currentLinkIndex + 1);
          }
        } else {
          // Fallback: navigate to next sibling
          navigateToNext();
        }
        event.preventDefault();
        break;

      case "ArrowLeft":
        if (hasNavigation) {
          // Navigate to parent if we're highlighting a parent link
          if (currentLinkIndex < parentLinks.length && parentLinks.length > 0) {
            window.location.href = parentLinks[currentLinkIndex].href;
          } else {
            // Otherwise navigate to first parent
            navigateToParent();
          }
        } else {
          // Fallback: navigate to parent
          navigateToParent();
        }
        event.preventDefault();
        break;

      case "ArrowRight":
        if (hasNavigation) {
          // Open the currently selected link
          const currentLinks = bbsLanguage === "en" ? allLinksEn : allLinksZh;
          if (
            currentLinks.length > 0 &&
            currentLinkIndex < currentLinks.length
          ) {
            window.location.href = currentLinks[currentLinkIndex].href;
          }
        }
        event.preventDefault();
        break;
    }
  });

  // Initialize navigation when page loads
  initializeNavigation();
});
