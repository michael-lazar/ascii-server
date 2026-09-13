document.addEventListener("DOMContentLoaded", function () {
  var msnry = new Masonry(".artgrid", {
    itemSelector: ".artgrid-item",
    // Column and gutter widths are defined in CSS on the sizer elements,
    // so the grid always fills the container and the media queries decide
    // the column count.
    columnWidth: ".artgrid-sizer",
    gutter: ".artgrid-gutter",
    percentPosition: true,
    transitionDuration: 200,
  });

  msnry.on("layoutComplete", function () {
    document.querySelector(".artgrid").style.visibility = "visible";
  });
  msnry.layout();
});
