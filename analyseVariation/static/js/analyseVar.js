const section2 = document.getElementById("section2");
const section3 = document.getElementById("section3");
const definirAction = document.getElementById("definir-action");
const ajoutAnalyse = document.getElementById("add-analyse");

const divPourquoi = document.getElementById("div-pourquoi");
const pourquoi = document.querySelectorAll("pourquois");
const pourquoiSuivant = document.getElementById("pourquoi-suivant");
var pourqw = document.querySelectorAll(".pourqw");

const pourquoi1=document.getElementById('pourquoi1');
var pourqw;

console.log("pourquoi : ",pourquoi);

ajoutAnalyse.addEventListener("click", (e) => {
  e.preventDefault()
  section2.classList.toggle("show2");
});

//definirAction.addEventListener("click", (e) => {
  //e.preventDefault()
  //section3.classList.toggle("show3");
//});

/*pourquoiSuivant.addEventListener("click", () => {
  //   var pourqw = document.querySelectorAll(".pourqw");
  const pourquoi = document.querySelectorAll(".pourquois");
  //   console.log(pourqw);
  console.log(divPourquoi.childNodes.length);
  let nbre = divPourquoi.childNodes.length - 1;
  const div = document.createElement("div");
  div.className = "row pourquoi mb-2 d-flex align-items-center border py-3";
  const label = document.createElement("label");
  label.className = "col-3 fs-3";
  label.innerText = "Pourquoi " + nbre;
  const divInput = document.createElement("div");
  divInput.className = "col-8 pourqw";
  divInput.id = "pourquoi_" + nbre;
  const input = document.createElement("input");
  input.className = "col-12";
  const divIcon = document.createElement("div");
  divIcon.className = "icon-add col-1 d-flex justify-content-end";
  const icon = document.createElement("i");
  icon.className = "fa-solid fa-circle-plus fs-4 pourquois";
  icon.style = "cursor: pointer";
  icon.id = "icon_" + nbre;

  divInput.append(input);
  divIcon.append(icon);
  div.append(label, divInput, divIcon);
  divPourquoi.append(div);

  // Pour les autres Pourquoi qu'on ajout à partir du button add:::::::::
  console.log(pourquoi.length);
  pourquoi.forEach((element) => {
    element.addEventListener("click", (e) => {
      const prq = e.target.parentElement.parentElement.children[1];
      const input = document.createElement("input");
      input.name = "pourquoi_" + nbre;
      input.className = "my-2";
      input.classList.add("col-12");
      input.type = "text";
      prq.appendChild(input);
    });
  });
});/*/

// Pour le premier Pourquoi qui apparait par défaut:::::::::
/*/pourquoi.forEach((element) => {
  element.addEventListener("click", (e) => {
    const prq = e.target.parentElement.parentElement.children[1];
    const input = document.createElement("input");
    input.name = "pourquoi2";
    input.className = "my-2";
    input.classList.add("col-12");
    input.type = "text";
    prq.appendChild(input);
  });
});/*/

////////////////////////////////////////////////////////////////////////

enregistrement_cause = document.getElementById('enregistrement_cause');
console.log('enreg ',enregistrement_cause)

var div_parent;
var duplique_input;
var labels;
function cre_boutton_plus_input(parent, id){
  duplique_input = document.createElement('div')
  //label = document.createElement('label')
  //label.textContent = `Pourquoi : ${i}`
  duplique_input.className = 'col-1 icon-add py-1 px-0'
  i = document.createElement('i')
  i.className = 'fa-solid fa-circle-plus fs-4 pourqois'
  duplique_input.setAttribute("id", `bouton_plus_${id}`)
  i.style.cursor = 'pointer'
  duplique_input.appendChild(i)
  parent.appendChild(duplique_input)
  //duplique_input.style.visibility = 'hidden'
}

function cre_bloc(parent, i){
  div_parent = document.createElement('div')
  Input = document.createElement('div')
  div_parent.className = 'col-12 d-flex row  mg-x-0'
  labels = document.createElement('label')
  labels.textContent = `Pourquoi : ${i}`
  labels.className = 'col-2 fs-5'
  divinput=document.createElement('div')
  input = document.createElement('input')
  divinput.className = 'col  pe-0 '
  Input.className = 'col d-flex row p-0'
  Input.style.justifyContent = 'space-between'
  input.className = 'col pe-0 me-2 fs-5'
  input.setAttribute('value', "")
  input.setAttribute('name', `input_${i}`)
  Input.setAttribute('id', `input_${i}`)
  Input.setAttribute('name', `input_${i}`)
  Input.appendChild(input)
  divinput.appendChild(Input)
  div_parent.appendChild(labels)
  div_parent.appendChild(divinput)
  div_parent.className = ' d-flex row'
  parent.appendChild(div_parent)
  var liste1 = []
  var liste2 = []
  if (i>=2){
    console.log('cool')
    cre_boutton_plus_input(divinput, i)
    id_bouton = document.getElementById(`bouton_plus_${i}`)
    id_input = document.getElementById(`input_${i}`)
    liste1.push(id_input)
    liste2.push(id_bouton)
    console.log('this ',id_input)
    liste1.forEach((elem)=>{
      //elem.addEventListener('click', (e)=>{
        //e.preventDefault()
        //console.log('this ',id_bouton, elem, liste1);
        liste2.forEach((el)=>{
          //el.style.visibility='visible';
          el.addEventListener('click', (e)=>{
            e.preventDefault()
            liste2 = liste2.filter((element) => element !== el)
            //liste1 = liste1.filter((element) => element !== elem)
            console.log('dfghj')
            //elem.firstChild.className='col-5'
            if (el.id=='bouton_plus_2'){
              cre_input(elem, 'input_21', 'input_21')
              console.log(el)
              el.style.visibility = 'hidden'
            }else if (elem.childNodes.length==4){
              el.style.visibility = 'hidden'
            }else {
              n=Number(elem.lastElementChild.id.split('_').pop())+1
              cre_input(elem, `input_${el.id.split('_').pop()+n}`, `input_${el.id.split('_').pop()+n}`)
              console.log(el.id.split('_').pop())
              console.log(n)
            }
          })
        })
        if (elem.id=='input_5') {
          // alert('Siuuus')
          divBt=document.getElementById('div-btn')
          //divBt.className='div-btn-show d-flex col-10 justify-content-between'
        }
      //})
    }) 
  }
}

function cre_input(parent, id, name){
  input = document.createElement('input')
  input.className = 'col me-2 fs-5'
  input.setAttribute('value', "")
  input.setAttribute('id', id)
  input.setAttribute('name', name)
  parent.appendChild(input)
}

function cre_boutton(parent){
  div = document.createElement('div')
  //label = document.createElement('label')
  //label.textContent = `Pourquoi : ${i}`
  div.className = 'col-1 icon-add'
  i = document.createElement('i')
  i.className = 'fa-solid fa-circle-plus fs-4 pourqois'
  i.setAttribute("id", "")
  i.style.cursor = 'pointer'
  div.appendChild(i)
  parent.appendChild(div)
  console.log(div)
  var i = parent.childNodes.length-1
  div.addEventListener('click', (e)=>{
    e.preventDefault();
    if (i<5){
      cre_bloc(enregistrement_cause, i)
      //console.log('plus',parent.childNodes.length-5, parent.lastElementChild.previousSibling, div_parent.previousSibling)
      parent.removeChild(div_parent.previousSibling)
      cre_boutton(enregistrement_cause);
    }else if(i==5){
      cre_bloc(enregistrement_cause, i)
      //console.log('plus',parent.childNodes.length-5, parent.lastElementChild.previousSibling, div_parent.previousSibling)
      parent.removeChild(div_parent.previousSibling)
    }
  })
}

valider = document.getElementById('bouton_valider_action')
valider.addEventListener('click', (e)=>{
  e.preventDefault()
})

//document.getElementById("enregistrement_de_detail").addEventListener('click', (e)=>{
//  e.preventDefault()
//  document.getElementById('div-btn').className='div-btn-show d-flex col-10 justify-content-between'
//})

//document.querySelectorAll('.definir_action').forEach((element)=>{
//  element.addEventListener('click', (e)=>{
//    e.preventDefault()
//  })
//})

// if (labels.textContent=="Pourquoi : 5") {
//   alert('okkk')
// }


var i = 1;
cre_bloc(enregistrement_cause, i);
cre_boutton(enregistrement_cause);

form = document.getElementById('form_action')
function sendData() {
  var XHR = new XMLHttpRequest();

  // Liez l'objet FormData et l'élément form
  var FD = new FormData(form);
  //FD.append(form)

  // Définissez ce qui se passe si la soumission s'est opérée avec succès
  XHR.addEventListener("load", function(event) {
    alert(event.target.responseText);
  });

  // Definissez ce qui se passe en cas d'erreur
  XHR.addEventListener("error", function(event) {
    alert('Oups! Quelque chose s\'est mal passé.');
  });

  // Configurez la requête
  XHR.open("POST", "http://127.0.0.1:5000/analyse_agent?reference=000012&n=9");

  // Les données envoyées sont ce que l'utilisateur a mis dans le formulaire
  XHR.send(FD);
  for (const [key, value] of FD) {
    console.log((`${key}: ${value}\n`));
    
  }
}

// Accédez à l'élément form …
var bouton_form = document.getElementById("bouton_form");

// … et prenez en charge l'événement submit.
/*bouton_form.addEventListener("click", function (event) {
  event.preventDefault();
  console.log("Hello!");
  sendData();
 
});*/