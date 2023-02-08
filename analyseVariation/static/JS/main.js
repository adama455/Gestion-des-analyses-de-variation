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

/* Ajout action individuel */
$('.definir-action').on('click', function (e) {
	e.preventDefault();
	$('#modal_action').modal('show');
	$(function () {
		$('[data-toggle="tooltip"]').tooltip()

	})
});
	


const form_actions = document.getElementById("form_actions");
const form_input = document.getElementById("form-input");
const recap_action = document.getElementById("recaputilatif");
const array = [];
document.getElementById("autre-act").addEventListener('click', ()=>{
	alert("Hello!");
	let i =form_input.childNodes.length -1 ;
	const H3 = document.createElement('h3');
	H3.innerHTML =`Action_n°${i}`
	H3.className ="modal-title fs-5 py-2"
	const div_ref =document.createElement("div");
	div_ref.className="col-3 d-flex flex-column"
	label_ref = document.createElement("label");
	label_ref.for="reference_action"
	label_ref.className="d-flex justify-content-start"
	label_ref.innerHTML = 'Ref action'
	input_ref = document.createElement("input");
	input_ref.className='fs-5'
	input_ref.id= 'reference_action'
	input_ref.name= 'reference_action'
	div_ref.appendChild(label_ref);
	div_ref.appendChild(input_ref);
	const div_lib =document.createElement("div");
	div_lib.className="col-3 d-flex flex-column"
	label_lib = document.createElement("label");
	label_lib.for="libelle_action"
	label_lib.className="d-flex justify-content-start"
	label_lib.innerHTML = 'Libelle Action'
	input_lib = document.createElement("input");
	input_lib.className='fs-5'
	input_lib.id= 'libelle_action'
	input_lib.name= 'libelle_action'
	div_lib.appendChild(label_lib);
	div_lib.appendChild(input_lib);
	const div_porteur =document.createElement("div");
	div_porteur.className="col-3 d-flex flex-column"
	label_porteur = document.createElement("label");
	label_porteur.for="porteur_action"
	label_porteur.className="d-flex justify-content-start"
	label_porteur.innerHTML = 'Porteur Action'
	input_porteur = document.createElement("input");
	input_porteur.className='fs-5'
	input_porteur.id= 'porteur_action'
	input_porteur.name= 'porteur_action'
	div_porteur.appendChild(label_porteur);
	div_porteur.appendChild(input_porteur);
	const div_echeance =document.createElement("div");
	div_echeance.className="col-3 d-flex flex-column"
	label_echeance = document.createElement("label");
	label_echeance.for="echeance_action"
	label_echeance.className="d-flex justify-content-start"
	label_echeance.innerHTML = 'Echeance'
	input_echeance = document.createElement("input");
	input_echeance.className='fs-5'
	input_echeance.id= 'echeance_action'
	input_echeance.name= 'echeance_action'
	input_echeance.type= 'date'
	div_echeance.appendChild(label_echeance);
	div_echeance.appendChild(input_echeance);
	
	const row = document.createElement("div");
	row.className="row mb-3"
	row.id="row_action"
	row.append(H3,div_ref,div_lib,div_porteur,div_echeance);
	form_input.appendChild(row);
	
	// array.splice(row);
	// console.log(array);
	array.push(row);
	console.log(array);
	// form_actions.appendChild(row)
})
/* Récaputilatif */
const row_actions =document.getElementById('row_action');
console.log(row_actions);
const row_recap = document.createElement('div');
const hr = document.createElement('hr');
const div1 = document.createElement('div');
const h2 = document.createElement('h2');
const div2 = document.createElement('div');
const h3 = document.createElement('h3');
document.getElementById('bouton_valider_action').addEventListener('click', ()=>{
	if (row_recap.parentElement!=null) {
		//row_recap.parentElement.remove()
		div1.removeChild(h2)
		div2.removeChild(h3)
		row_recap.removeChild(div1,div2)
		recap_action.removeChild(row_recap,hr)

		alert('okk!')
	}
	array.forEach(element => {
		
		row_recap.className ="row pourquoi51 d-flex justify-content-center align-items-center";
		div1.className = "col-3"
		h2.innerHTML='pourquoi51';
		div1.appendChild(h2);
		div2.className = "col-9"
		h3.innerHTML='Actions P51';
		hr.className ="border border-secondary"
		form_input.append(element)
		div2.append(h3, element);
		row_recap.append(div1,div2)
		recap_action.append(row_recap,hr)
		
	});
	
});

bntAutreAct = document.getElementById('btn_autre_action')
autreAction = document.getElementById('autre_action')
bntAutreAct.addEventListener('click', ()=>{
	autreAction.classList.toggle('autre_action_show')
	document.getElementById('reference_autre_action').value = document.getElementById('reference_action').value+'2'
})

// definir_action = document.querySelectorAll('.definir_action');
// definir_action.forEach((def_act) => {
// 	def_act.addEventListener('click',(e)=>{
// 		e.preventDefault();
// 		for (let i = 0; i < 10; i++) {	
// 			console.log(
// 				document.getElementById('reference_av_act').value+document.getElementById('identifiant_act').value+`P${i}ACT1`
// 			);
// 			document.getElementById('reference_action').value = document.getElementById('reference_av_act').value+document.getElementById('identifiant_act').value+`P${i}ACT1`
// 		}
// 	})
// });

document.getElementById('action1').addEventListener('click', (e)=>{
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
})
