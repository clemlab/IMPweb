function check_navbar_active() {
  $(".nav").find(".active").removeClass("active");
  $(this).parent().addClass("active");

  // if above didn't work
  if ($(".nav").find(".active").length == 0) {
    var pathname = window.location.pathname;
    $('.nav > li > a[href="'+pathname+'"]').parent().addClass('active');
  }
}

$(document).ready(check_navbar_active);
$(".nav a").on("click", check_navbar_active);
