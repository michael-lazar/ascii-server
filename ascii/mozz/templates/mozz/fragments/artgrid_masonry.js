document.addEventListener("DOMContentLoaded", function () {
  var msnry = new Masonry(".artgrid", {
    columnWidth: 176,
    itemSelector: ".artgrid-item",
    transitionDuration: 200,
    gutter: 20,
    // Size the container to the columns that fit, so the grid can be
    // centered with margin: auto instead of leaving a gap on the right.
    fitWidth: true,
  });

  msnry.on("layoutComplete", function () {
    document.querySelector(".artgrid").style.visibility = "visible";
  });
  msnry.layout();

  // Masonry's own resize handling doesn't reliably shrink a fitWidth grid
  // back down, so force a relayout after the window settles.
  let resizeTimeout;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => msnry.layout(), 100);
  });
});
