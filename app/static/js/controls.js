require(["jquery"], function($) { 

$("body").keyup(function(e){
  if (e.keyCode == 13) {
    const mode = $('.mode-nav-item.active').text()
    $(`.${mode} button.refresh`).click();
  }
});

$("li#random-tab").click(function() {
  $('.random').css({display: 'block'});
  $('.top').css({display: 'none'});

  $('li#random-tab').addClass('active');
  $('li#top-tab').removeClass('active');
});

$("li#top-tab").click(function() {
  $('.top').css({display: 'block'});
  $('.random').css({display: 'none'});

  $('li#random-tab').removeClass('active');
  $('li#top-tab').addClass('active');
});

});