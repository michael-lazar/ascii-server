const breakpoint = 768;

document.addEventListener("DOMContentLoaded", function () {
  let isAboveBreakpoint = window.innerWidth > breakpoint;

  var msnry = new Masonry(".artfile-grid", {
    columnWidth: 170,
    itemSelector: ".artfile-card",
    transitionDuration: 200,
    gutter: 20,
    // fitWidth doesn't seem to work with my large screen css for some reason,
    // it will resize when the window is being dragged larger, but won't scale
    // back down when the window shrinks. So I'm only turning this on for
    // mobile so the grid will be centered on the screen.
    fitWidth: !isAboveBreakpoint,
  });

  function layoutComplete() {
    var grid = document.querySelector(".artfile-grid");
    grid.style.visibility = "visible";
  }

  msnry.on("layoutComplete", layoutComplete);
  msnry.layout();

  function handleResize() {
    const newIsAboveBreakpoint = window.innerWidth > breakpoint;

    // Check if we've crossed the breakpoint since the last resize event
    if (newIsAboveBreakpoint !== isAboveBreakpoint) {
      msnry.destroy();
      msnry = new Masonry(".artfile-grid", {
        columnWidth: 170,
        itemSelector: ".artfile-card",
        transitionDuration: 200,
        gutter: 20,
        fitWidth: !newIsAboveBreakpoint,
      });

      // Update the tracking variable
      isAboveBreakpoint = newIsAboveBreakpoint;
    }
  }

  // Debounce the resize function to avoid excessive calls
  let resizeTimeout;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(handleResize, 1);
  });

  document.body.addEventListener("htmx:oobAfterSwap", function (evt) {
    var newElements = evt.detail.target.querySelectorAll(".htmx-added");
    msnry.appended(newElements);
  });

  document.addEventListener("htmx:afterRequest", function (evt) {
    var button = $("#paginationLoadMore");

    button.click(function () {
      button.text("Loading...");
      button.attr("disabled", "disabled");
    });
  });

  $(document).ready(function () {
    var button = $("#paginationLoadMore");
    button.click(function () {
      button.text("Loading...");
      button.attr("disabled", "disabled");
    });
  });
});
