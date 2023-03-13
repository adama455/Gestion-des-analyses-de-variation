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
  input_ref.className = "fs-5";
  input_ref.id = `${id}_${n}.${i}`;
  // console.log(input_ref.id);
  input_ref.name = `${id}_${n}.${i}`;
  //alert(label)
  if (label == "Ref Action") {
    input_ref.value = `${id}_${n}.${i}`;
  }
  if (label == "Echeance Action") {
    input_ref.type = "date";
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
  var id_va = url.searchParams.get("id_va");
  var fichier_id = url.searchParams.get("fichier_id");
  url = Url +'?fichier_id='+fichier_id+'&id_va='+id_va
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
    document.getElementById(`input_5${index}_act`).value
    causes_racines.push(document.getElementById(`input_5${index}_act`).value)
  }
  sessionStorage.setItem('causes_racines',causes_racines)
})
