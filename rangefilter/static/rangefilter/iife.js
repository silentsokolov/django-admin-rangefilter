(function() {
  'use strict';
  django.jQuery(".admindatefilter").each(
    function(){
      var form_id = django.jQuery(this).find("form").attr('id').slice(0,-5);
      var qs_name = form_id+"-query-string";
      var query_string = django.jQuery('input#'+qs_name).val();
      var form_name = form_id+"-form";

      // Bind submit buttons
      django.jQuery(this).find("input[type=select]").bind("click",
        function(event){
          event.preventDefault();
          var form_data = django.jQuery('#'+form_name).serialize();
          window.location = window.location.pathname + query_string + '&' + form_data;
      });

      // Bind reset buttons
      django.jQuery(this).find("input[type=reset]").bind("click",
        function(){
          window.location = window.location.pathname + query_string;
      });
    });
})();
