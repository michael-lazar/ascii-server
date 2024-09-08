document.addEventListener("DOMContentLoaded", function() {
  var form = document.getElementById("packFilterForm");
  form.addEventListener("change", function() {
    form.submit();
  });

  var clearButtons = document.querySelectorAll(".sidebar-legend-clear");
  clearButtons.forEach(function(button) {
    button.addEventListener("click", function() {
      var fieldset = button.closest("fieldset");
      var inputs = fieldset.querySelectorAll("input:not([type='submit']), select, textarea");
      inputs.forEach(function(input) {
        if (input.type === "checkbox" || input.type === "radio") {
          input.checked = false;
        } else {
          input.value = "";
        }
        if (input.tagName === "SELECT") {
          input.selectedIndex = 0;
        }
      });

      form.submit();
    });
  });

});
