const breakpoint = 600;

function buildArtgrid(isMobile) {
  if (isMobile) {
    // Below the breakpoint the cards are styled width: 100% and stack in
    // a single fluid column, so masonry measures the element width.
    // fitWidth doesn't support element sizing, but there is nothing to
    // center in a full-width column anyway.
    return new Masonry(".artgrid", {
      itemSelector: ".artgrid-item",
      columnWidth: ".artgrid-item",
      transitionDuration: 200,
    });
  }
  return new Masonry(".artgrid", {
    itemSelector: ".artgrid-item",
    columnWidth: 264,
    gutter: 12,
    transitionDuration: 200,
    // Size the container to the columns that fit, so the grid can be
    // centered with margin: auto instead of leaving a gap on the right.
    fitWidth: true,
  });
}

document.addEventListener("DOMContentLoaded", function () {
  let isMobile = window.innerWidth <= breakpoint;

  var msnry = buildArtgrid(isMobile);
  msnry.on("layoutComplete", function () {
    document.querySelector(".artgrid").style.visibility = "visible";
  });
  msnry.layout();

  // Masonry's own resize handling doesn't reliably shrink a fitWidth grid
  // back down, so force a relayout after the window settles, and rebuild
  // the grid when the mobile breakpoint is crossed.
  let resizeTimeout;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      const newIsMobile = window.innerWidth <= breakpoint;
      if (newIsMobile !== isMobile) {
        isMobile = newIsMobile;
        msnry.destroy();
        msnry = buildArtgrid(isMobile);
      }
      msnry.layout();
    }, 100);
  });
});
