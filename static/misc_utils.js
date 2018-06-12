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

function randomize_order() {
  var cards = $(".team-col");
  for(var i = 0; i < cards.length; i++){
      var target = Math.floor(Math.random() * cards.length -1) + 1;
      var target2 = Math.floor(Math.random() * cards.length -1) +1;
      cards.eq(target).before(cards.eq(target2));
  }
}
$(document).ready(randomize_order);
