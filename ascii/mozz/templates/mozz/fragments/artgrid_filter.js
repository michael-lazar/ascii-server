document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("artgridFilterForm");
  form.addEventListener("change", function () {
    form.submit();
  });
});
