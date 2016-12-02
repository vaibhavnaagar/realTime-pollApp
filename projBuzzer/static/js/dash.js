$('.section-header').on('click', function (){
  $(this).toggleClass('is-active').next('div').slideToggle();
})
