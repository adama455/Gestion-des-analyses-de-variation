(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
      $('#sidebar').toggleClass('active');
  });

})(jQuery);

/*POPUP DE CHARGEMENT DU FICHIER*/

$('#demarrav').on('click', function(e) {  
	e.preventDefault();           
	$('#loginModal').modal('show');
  	$(function () {
    	$('[data-toggle="tooltip"]').tooltip()
  })
});


$('#adduser').on('click', function(e) {  
	e.preventDefault();           
	$('#adduserModal').modal('show');
  	$(function () {
    	$('[data-toggle="tooltip"]').tooltip()
  })
});