(
  // Code below makes sure that the DateTimeShortcuts.js is loaded exactly once
  // regardless the presence of AdminDateWidget
  // How it worked:
  //  - First Django loads the model formset with predefined widgets for different
  //    field types. If there's a date based field, then it loads the AdminDateWidget
  //    and it's required media to context under {{media.js}} in admin/change_list.html.
  //    (Note: it accumulates media in django.forms.widgets.Media object,
  //    which prevents duplicates, but the DateRangeFilter is not included yet
  //    since it's not model field related.
  //    List of predefined widgets is in django.contrib.admin.options.FORMFIELD_FOR_DBFIELD_DEFAULTS)
  //  - After that Django starts rendering forms, which have the {{form.media}}
  //    tag. Only then the DjangoRangeFilter.get_media is called and rendered,
  //    which creates the duplicates.
  // How it works:
  //  - first step is the same, if there's a AdminDateWidget to be loaded then
  //    nothing changes
  //  - DOM gets rendered and if the AdminDateWidget was rendered then
  //    the DateTimeShortcuts.js is initiated which sets the window.DateTimeShortcuts.
  //    Otherwise, the window.DateTimeShortcuts is undefined.
  //  - The lines below check if the DateTimeShortcuts has been set and if not
  //    then the DateTimeShortcuts.js and calendar.js is rendered
  //
  //  https://github.com/silentsokolov/django-admin-rangefilter/issues/9
  //
  // Django 2.1
  //  https://github.com/silentsokolov/django-admin-rangefilter/issues/21
  django.jQuery('document').ready(function () {
      if (!('DateTimeShortcuts' in window)) {
          django.jQuery.when(

              django.jQuery.getScript('/static/admin/js/admin/DateTimeShortcuts.js'),

              django.jQuery.getScript('/static/admin/js/calendar.js'),

              django.jQuery.Deferred(function( deferred ){
                  django.jQuery( deferred.resolve );
              })
          ).done(function(){
              django.jQuery('.datetimeshortcuts').remove();
              DateTimeShortcuts.init();
          });
      }
  });

  django.jQuery(".admindatefilter").each(
    function(){
      var form_id = $(this).find("form").attr('id');
      var query_name = form_id+"-query-string";
      var form_name = form_id+"-form";

      // Bind submit buttons
      $(this).find("input[type=select]").bind("click",
        function(event){
          event.preventDefault();
          var query_string = django.jQuery('input#'+query_name).val();
          var form_data = django.jQuery('#'+form_name).serialize();
          window.location = window.location.pathname + query_string + '&' + form_data;
      });

      // Bind reset buttons
      $(this).find("input[type=reset]").bind("click",
        function(){
          var query_string = django.jQuery('input#'+qs_name).val();
          window.location = window.location.pathname + query_string;
      });

    });
)()
