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

$('#changepwd').on('click', function(e) {  
	e.preventDefault();           
	$('#profil').modal('show');
  	$(function () {
    	$('[data-toggle="tooltip"]').tooltip()
  })
});

$('#addcause').on('click', function(e) {  
	e.preventDefault();           
	$('#addCauseModal').modal('show');
  	$(function () {
    	$('[data-toggle="tooltip"]').tooltip()
  })
});
$('#addPlateau').on('click', function(e) {  
	e.preventDefault();           
	$('#addPlateauModal').modal('show');
  	$(function () {
    	$('[data-toggle="tooltip"]').tooltip()
  })
});

$('.definir-action').on('click', function (e) {
	e.preventDefault();
	$('#modal_action').modal('show');
	$(function () {
		$('[data-toggle="tooltip"]').tooltip()
	})
});

bntAutreAct = document.getElementById('btn_autre_action')
autreAction = document.getElementById('autre_action')
bntAutreAct.addEventListener('click', ()=>{
	autreAction.classList.toggle('autre_action_show')
	document.getElementById('reference_autre_action').value = document.getElementById('reference_action').value+'2'
})

/*/document.getElementById('action1').addEventListener('click', (e)=>{
	//e.preventDefault()
	document.getElementById('reference_action').value = document.getElementById('reference_av_act').value+document.getElementById('identifiant_act').value+'P1ACT1'
})

document.getElementById('action2').addEventListener('click', (e)=>{
	e.preventDefault()
	document.getElementById('reference_action').value = document.getElementById('reference_av_act').value+document.getElementById('identifiant_act').value+'P2ACT1'
})

document.getElementById('action3').addEventListener('click', (e)=>{
	e.preventDefault()
	document.getElementById('reference_action').value = document.getElementById('reference_av_act').value+document.getElementById('identifiant_act').value+'P3ACT1'
})

document.getElementById('action4').addEventListener('click', (e)=>{
	e.preventDefault()
	document.getElementById('reference_action').value = document.getElementById('reference_av_act').value+document.getElementById('identifiant_act').value+'P4ACT1'
})/*/