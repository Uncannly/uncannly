$("body").keyup(function(e){
  if (e.keyCode == 13) {
    const mode = $("input[name='mode']:checked").val()
    $(`.${mode} button.refresh`).click();
  }
});

$("input[name='mode']").change(function(e){
  if($(this).val() == 'random') {
    $('.random').css({display: 'block'});
    $('.top').css({display: 'none'});
  } else {
    $('.top').css({display: 'block'});
    $('.random').css({display: 'none'});
  }
});