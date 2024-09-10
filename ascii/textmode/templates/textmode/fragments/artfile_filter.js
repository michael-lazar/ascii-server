document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("packFilterForm");
  form.addEventListener("change", function () {
    form.submit();
  });
});
