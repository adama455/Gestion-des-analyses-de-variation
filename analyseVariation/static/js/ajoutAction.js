////////////////////////////////////////////////////////////////////////

enregistrement_cause = document.getElementById("enregistrement_action");
console.log("enreg ", enregistrement_cause);

/* Ajout action individuel */

var div_parent;
var duplique_input;
var labels;
function cre_boutton_plus_input(parent, id) {
  duplique_input = document.createElement("div");
  duplique_input.className = "col-1 icon-add py-1 px-0";
  i = document.createElement("i");
  i.className = "fa-solid fa-circle-plus fs-4 pourqois";
  duplique_input.setAttribute("id", `bouton_plus_${id}`);
  i.style.cursor = "pointer";
  duplique_input.appendChild(i);
  parent.appendChild(duplique_input);
}

function cre_bloc(parent, i) {
  div_parent = document.createElement("div");
  div_Input = document.createElement("div");
  div_button = document.createElement("div");
  div_parent.className = "col-12 d-flex row  mg-x-0";
  div_button.className = "col d-flex row ";
  labels = document.createElement("label");
  labels.textContent = `Pourquoi : ${i}`;
  labels.className = "col-2 fs-5";
  div_input_button = document.createElement("div");
  input = document.createElement("input");
  div_input_button.className = "col  pe-0 ";
  div_Input.className = "col d-flex row p-0";
  div_Input.style.justifyContent = "space-between";
  input.className = "col pe-0 me-2 fs-5";
  input.setAttribute("value", "");
  input.setAttribute("name", `input_${i}`);
  div_Input.setAttribute("id", `input_${i}`);
  div_Input.setAttribute("name", `input_${i}`);
  div_Input.appendChild(input);
  div_input_button.appendChild(div_Input);
  div_input_button.appendChild(div_button);
  div_parent.appendChild(labels);
  div_parent.appendChild(div_input_button);
  div_parent.className = " d-flex row";
  parent.appendChild(div_parent);
  /*/  var liste1 = []
  var liste2 = []
  var liste3 = []
  //if (i>=2){
    console.log('cool')
    cre_boutton_plus_input(div_button, i)
    cre_boutton_moins_input(div_button, i)
    id_bouton_plus = document.getElementById(`bouton_plus_${i}`)
    id_bouton_moins = document.getElementById(`bouton_moins_${i}`)
    id_input = document.getElementById(`input_${i}`)
    liste1.push(id_input)
    liste2.push(id_bouton_plus)
    liste3.push(id_bouton_moins)
    console.log('this ',id_input)
    liste1.forEach((elements)=>{
      liste3.forEach((el)=>{
        liste2.forEach((elem)=>{
          ///Ecouter chaque bouton plus pour ajouter des input au besoin
          elem.addEventListener('click', (e)=>{
            e.preventDefault()
            liste2 = liste2.filter((element) => element !== elem)
            if (elements.childNodes.length>=1){
              el.style.visibility = 'visible'
            }
            if (elements.childNodes.length==10){
              elem.style.visibility = 'hidden'
            }else {
              n=Number(elements.lastElementChild.id.split('_').pop())+1
              cre_input(elements, `input_${elem.id.split('_').pop()+n}`, `input_${elem.id.split('_').pop()+n}`)
            }
          })

          ////Ecouter chaque bouton moin pour pouvoir supprimer des inputs
        el.addEventListener('click', (e)=>{
          e.preventDefault()
          if (elements.childNodes.length<=2){
            el.style.visibility = 'hidden'
            console.log('n',elements.childNodes.length);
          }
          elem.style.visibility = 'visible'
          elements.removeChild(elements.lastElementChild)
          liste3 = liste3.filter((element) => element !== el)
          n=Number(elements.lastElementChild.id.split('_').pop())+1
        })

      })
    })

        if (elements.id=='input_5') {
          divBt=document.getElementById('div-btn')
          for (let i = 1; i < 5; i++) {
           bloc_pourquoi = document.getElementById(`input_${i}`)
           nbre_fils = bloc_pourquoi.childNodes.length
           console.log(nbre_fils)
          }
        }
    }) /*/
}

function cre_input(parent, id, name) {
  input = document.createElement("input");
  input.className = "col me-2 fs-5";
  input.setAttribute("value", "");
  input.setAttribute("id", id);
  input.setAttribute("name", name);
  parent.appendChild(input);
}

function cre_boutton(parent) {
  div = document.createElement("div");
  div.className = "col-1 icon-add";
  i = document.createElement("i");
  i.className = "fa-solid fa-circle-plus fs-4 pourqois";
  i.setAttribute("id", "");
  i.style.cursor = "pointer";
  div.appendChild(i);
  parent.appendChild(div);
  console.log(div);
  var i = parent.childNodes.length - 1;
  /*/div.addEventListener('click', (e)=>{
    e.preventDefault();
    if (i<5){
      cre_bloc(enregistrement_cause, i)
      parent.removeChild(div_parent.previousSibling)
      cre_boutton(enregistrement_cause);
    }else if(i==5){
      cre_bloc(enregistrement_cause, i)
      parent.removeChild(div_parent.previousSibling)
      
    }
  })/*/
}

function cre_boutton_moins_input(parent, id) {
  delete_input = document.createElement("div");
  delete_input.className = "col-1 icon-add py-1 px-0";
  i = document.createElement("i");
  i.className = "fa-solid fa-circle-minus fs-4 pourqois";
  i.style.cursor = "pointer";
  delete_input.setAttribute("id", `bouton_moins_${id}`);
  delete_input.appendChild(i);
  delete_input.style.visibility = "hidden";
  parent.appendChild(delete_input);
}

valider = document.getElementById("bouton_valider_action");
valider.addEventListener("click", (e) => {
  e.preventDefault();
});

/*/document.getElementById("enregistrement_de_detail").addEventListener('click', (e)=>{
  //e.preventDefault()
  divBt=document.getElementById('div-btn')
      for (let i = 1; i < 5; i++) {
        bloc_pourquoi = document.getElementById(`input_${i}`)
       //nbre_fils = bloc_pourquoi.childNodes.length
       console.log(bloc_pourquoi)
      }
})/*/

//var i = 1;
/*/for (let index = 1; index < 6; index++) {
  //const element = array[index];
  cre_bloc(enregistrement_cause, index);
  id_input = document.getElementById(`input_${index}`)
  //console.log(i,id_input);
  n = Number(localStorage.getItem(`pourquoi${index}`))
  test = localStorage.getItem('test')
  //n=Number(id_input.lastElementChild.id.split('_').pop())+1
  console.log(n, test);
  for (let j = 1; j < n; j++) {
    cre_input(id_input, `input_${index}${j}`, `input_${index}${j}`)
  }
}/*/

//cre_boutton(enregistrement_cause);

//form = document.getElementById('form_action')

// Accédez à l'élément form …
var bouton_form = document.getElementById("bouton_form");

//////////////////////////////////---MODAL ACTION---/////////////////////////////

var liste_labelle = [
  "Ref Action",
  "Libelle Action",
  "Porteur Acton",
  "Echeance Action",
];
var liste_id = [
  "reference_action",
  "libelle_action",
  "porteur_action",
  "echeance_action",
];
var data_acton = [];

function sous_bloc_action(parent, n, i, id, label) {
  const div_ref = document.createElement("div");
  div_ref.className = "col-3 d-flex flex-column";
  label_ref = document.createElement("label");
  label_ref.for = `${id}_${n}.${i}`;
  label_ref.className = "d-flex justify-content-start";
  label_ref.innerHTML = label;
  input_ref = document.createElement("input");
  input_ref.className = "fs-5 ps-2";
  input_ref.id = `${id}_${n}.${i}`;
  // console.log(input_ref.id);
  input_ref.name = `${id}_${n}.${i}`;
  //alert(label)
  if (label == "Ref Action") {
    input_ref.value = `${id}_${n}.${i}`;
  }
  if (label == "Libelle Action") {
    div_ref.className = "col-5 d-flex flex-column";
  }
  if (label == "Porteur Acton") {
    div_ref.className = "col-2 d-flex flex-column";
  }
  if (label == "Echeance Action") {
    input_ref.type = "date";
    div_ref.className = "col-2 d-flex flex-column";
  }

  div_ref.appendChild(label_ref);
  div_ref.appendChild(input_ref);
  parent.appendChild(div_ref);
}

function bloc_actions(parent, n) {
  var i = form_input.childNodes.length;
  const H3 = document.createElement("h3");
  H3.innerHTML = `Action_n°${i}`;
  H3.className = "modal-title fs-5 py-2";
  const row = document.createElement("div");
  row.className = "row mb-3";
  row.id = `row_action_${n}`;
  row.append(H3);
  for (let index = 0; index < 4; index++) {
    sous_bloc_action(row, n, i, liste_id[index], liste_labelle[index]);
  }
  parent.appendChild(row);
}

const form_actions = document.getElementById("form_actions");
const form_input = document.getElementById("form-input");
const recap_action = document.getElementById("recaputilatif");
const array = [];

/*/
function bloc_action(n){
	let i =form_input.childNodes.length -1 ;
	const H3 = document.createElement('h3');
	H3.innerHTML = `Action_n°${i+1}`
	H3.className = "modal-title fs-5 py-2"
	const div_ref =document.createElement("div");
	div_ref.className="col-3 d-flex flex-column"
	label_ref = document.createElement("label");
	label_ref.for=`reference_action_${n}${i+1}`
	label_ref.className="d-flex justify-content-start"
	label_ref.innerHTML = 'Ref action'
	input_ref = document.createElement("input");
	input_ref.className='fs-5'
	input_ref.id= `reference_action_${n}${i+1}`
	input_ref.name= `reference_action_${n}${i+1}`
	input_ref.value= `reference_action_${n}${i+1}`
	div_ref.appendChild(label_ref);
	div_ref.appendChild(input_ref);
	const div_lib =document.createElement("div");
	div_lib.className="col-3 d-flex flex-column"
	label_lib = document.createElement("label");
	label_lib.for=`libelle_action_${n}${i+1}`
	label_lib.className="d-flex justify-content-start"
	label_lib.innerHTML = 'Libelle Action'
	input_lib = document.createElement("input");
	input_lib.className='fs-5'
	input_lib.id= `libelle_action_${n}${i+1}`
	input_lib.name= `libelle_action_${n}${i+1}`
	div_lib.appendChild(label_lib);
	div_lib.appendChild(input_lib);
	const div_porteur =document.createElement("div");
	div_porteur.className="col-3 d-flex flex-column"
	label_porteur = document.createElement("label");
	label_porteur.for=`porteur_action_${n}${i+1}`
	label_porteur.className="d-flex justify-content-start"
	label_porteur.innerHTML = 'Porteur Action'
	input_porteur = document.createElement("input");
	input_porteur.className='fs-5'
	input_porteur.id= `porteur_action_${n}${i+1}`
	input_porteur.name= `porteur_action_${n}${i+1}`
	div_porteur.appendChild(label_porteur);
	div_porteur.appendChild(input_porteur);
	const div_echeance =document.createElement("div");
	div_echeance.className="col-3 d-flex flex-column"
	label_echeance = document.createElement("label");
	label_echeance.for=`echeance_action_${n}${i+1}`
	label_echeance.className="d-flex justify-content-start"
	label_echeance.innerHTML = 'Echeance'
	input_echeance = document.createElement("input");
	input_echeance.className='fs-5'
	input_echeance.id= `echeance_action_${n}${i+1}`
	input_echeance.name= `echeance_action_${n}${i+1}`
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
}
/*/

document.querySelectorAll(".definir_action").forEach((element) => {
  //element.addEventListener('click', ()=>{
    
  $(element).on('click', function (e) {
      e.preventDefault();
      console.log(element);
      var k = element.getAttribute('id').split('_').pop()
      var modal_title = document.getElementById(`input_5${k}_act`).value
      title = document.getElementById('modal_title')
      title.innerHTML = `Pourquoi 5${k} : `+ modal_title
      method = 'POST'
      data = 'reference_action_11'
      url = "http://127.0.0.1:5000/ajouter_action"
      console.log(url)
      // ajax(method, data, url)
      $('#modal_action').modal('show');
      $(function () {
        $('[data-toggle="tooltip"]').tooltip()
        bloc_actions(form_input, k);
        document.getElementById("autre-act").addEventListener('click', ()=>{
          bloc_actions(form_input, element.getAttribute('id').split('_').pop());
        })
      })
  })
});

function ajax(method, data, Url) {
  var url = new URL(window.location.href);
  var id = document.getElementById("identifiant_act").value;
  console.log(id);
  var reference = document.getElementById("reference_av_act").value;
  var n = url.searchParams.get("n");
  url = Url +'?reference='+reference+'&n='+n+'&id='+id
  console.log(url)
  $.ajax({
    data: { data: data }, //grab text between span tags
    type: method,
    url: url, //post grabbed text to flask endpoint for saving role
    async: false,
    success: function (data) {
      console.log("Sent Successfully", url);
    },
    error: function (e) {
      console.log("Submission failed...");
    },
  });
}


var ACTION = [];
var test = ["encore testons"];
$(document).ready(function () {
  $("#bouton_valider_action").click(function (event) {
    //event.preventDefault();
    var nbre = document.getElementById("form-input").childNodes;
    for (let i = 1; i < nbre.length; i++) {
      var action = [];
      for (let j = 1; j < nbre[i].childNodes.length; j++) {
        //const element = array[j];
        action.push(nbre[i].childNodes[j].lastChild.value);
        console.log(nbre[i].childNodes[j].lastChild.value);
      }
      ACTION.push(action);
      action.push("|");
      console.log(ACTION);
    }
    method = "POST";
    data = ACTION.toString();
    url = "http://127.0.0.1:5000/ajouter_action";
    ajax(method, data, url);
    //window.location.reload();
  });
});

var element_statut_terminer = ['']
var element_courant
var exist
document.getElementById('enregistrement_de_detail').addEventListener('click', (e)=>{
  // e.preventDefault()
  alert('Voulez vous reellement terminer cette analyse ?')
  element_statut_terminer = sessionStorage.getItem('element_statut_terminer')
  if (element_statut_terminer){
    element_statut_terminer = element_statut_terminer.split(',')
    console.log(element_statut_terminer)
    element_statut_terminer.forEach((element)=>{
      if (element==element_courant){
        exist = 1
      }
    })
  }else {
    element_statut_terminer = ['']
  }
  if (exist!=1){
  element_courant = sessionStorage.getItem('element_courant')
    element_statut_terminer.push(element_courant)
  }
  sessionStorage.setItem('element_statut_terminer', element_statut_terminer)
})

console.log(document.getElementById('libelle_av').value)

document.getElementById('action_programme').firstElementChild.addEventListener('click', (e)=>{
  // e.preventDefault()
  var causes_racines = []
  causes_racines.push(document.getElementById('libelle_av').value)
  for (let index = 1; index < 7; index++) {
    if (document.getElementById(`input_5${index}_act`).value != "") {
      document.getElementById(`input_5${index}_act`).value
      causes_racines.push(document.getElementById(`input_5${index}_act`).value)
    }
  }
  sessionStorage.setItem('causes_racines',causes_racines)
})

// console.log(terminer)

/////////////////////////* Récaputilatif *//////////////////////////////////
/*/const row_actions =document.getElementById('row_action');
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
	
});/*/
/*/
bntAutreAct = document.getElementById('btn_autre_action')
autreAction = document.getElementById('autre_action')
bntAutreAct.addEventListener('click', ()=>{
	autreAction.classList.toggle('autre_action_show')
	document.getElementById('reference_autre_action').value = document.getElementById('reference_action').value+'2'
})/*/
