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


////////////////////////////////////////////////////////////////////////

enregistrement_cause = document.getElementById('enregistrement_cause');
console.log('enreg ',enregistrement_cause)

var div_parent;
var duplique_input;
var labels;
function cre_boutton_plus_input(parent, id){
  duplique_input = document.createElement('div')
  duplique_input.className = 'col-1 icon-add py-1 px-0'
  i = document.createElement('i')
  i.className = 'fa-solid fa-circle-plus fs-4 pourqois'
  duplique_input.setAttribute("id", `bouton_plus_${id}`)
  i.style.cursor = 'pointer'
  duplique_input.appendChild(i)
  parent.appendChild(duplique_input)
}

function cre_bloc(parent, i){
  div_parent = document.createElement('div')
  div_Input = document.createElement('div')
  div_button = document.createElement('div')
  div_parent.className = 'col-12 d-flex row  mg-x-0'
  div_button.className = 'col d-flex row '
  labels = document.createElement('label')
  labels.textContent = `Pourquoi : ${i}`
  labels.className = 'col-2 fs-5'
  div_input_button=document.createElement('div')
  input = document.createElement('input')
  div_input_button.className = 'col  pe-0 '
  div_Input.className = 'col d-flex row p-0'
  div_Input.style.justifyContent = 'space-between'
  input.className = 'col pe-0 me-2 fs-5'
  input.setAttribute('value', "")
  input.setAttribute('name', `input_${i}`)
  input.setAttribute('id', `input_${i}`)
  div_Input.setAttribute('id', `input_${i}`)
  div_Input.setAttribute('name', `input_${i}`)
  div_Input.appendChild(input)
  div_input_button.appendChild(div_Input)
  div_input_button.appendChild(div_button)
  div_parent.appendChild(labels)
  div_parent.appendChild(div_input_button)
  div_parent.className = ' d-flex row'
  parent.appendChild(div_parent)
  var liste1 = []
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
    }) 
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
      parent.removeChild(div_parent.previousSibling)
      cre_boutton(enregistrement_cause);
    }else if(i==5){
      cre_bloc(enregistrement_cause, i)
      parent.removeChild(div_parent.previousSibling)
      localStorage.setItem('tests','1234')
    }
  })
}

function cre_boutton_moins_input(parent, id){
  delete_input = document.createElement('div')
  delete_input.className = 'col-1 icon-add py-1 px-0'
  i = document.createElement('i')
  i.className = 'fa-solid fa-circle-minus fs-4 pourqois'
  i.style.cursor = 'pointer'
  delete_input.setAttribute("id", `bouton_moins_${id}`)
  delete_input.appendChild(i)
  delete_input.style.visibility = 'hidden'
  parent.appendChild(delete_input)
}

valider = document.getElementById('bouton_valider_action')
valider.addEventListener('click', (e)=>{
  e.preventDefault()
})

localStorage.setItem('test','13')
//localStorage.removeItem('test')
var pourquoi_1 = []
var valeur_1 = []
var pourquoi_1 = []
var pourquoi_2 = []
var valeur_2 = []
var pourquoi_3 = []
var valeur_3 = []
var pourquoi_4 = []
var valeur_4 = []
var pourquoi_5 = []
var valeur_5 = []

document.getElementById("enregistrement_de_detail").addEventListener('click', (e)=>{
  //e.preventDefault()
  //divBt=document.getElementById('div-btn')
      for (let i = 1; i < 6; i++) {
        identifiant = document.getElementById('identifiant').value
        probleme = document.getElementById('probleme').value
        bloc_pourquoi = document.getElementById(`input_${i}`)
        nbre_fils = bloc_pourquoi.childNodes.length
        localStorage.setItem(`pourquoi${i}`,nbre_fils)
        localStorage.setItem('tests','1234')
        if (i==1){
          console.log(bloc_pourquoi.childNodes)
          bloc_pourquoi.childNodes.forEach((elem)=>{
            console.log(elem.getAttribute('id'),elem.value);
            var id = elem.getAttribute('id')
            pourquoi_1.push(elem.getAttribute('id'))
            valeur_1.push(elem.value)
            var valeur = elem.value
            console.log(pourquoi);
          })
        }else if (i==2) {
          console.log(bloc_pourquoi.childNodes)
          bloc_pourquoi.childNodes.forEach((elem)=>{
            console.log(elem.getAttribute('id'),elem.value);
            var id = elem.getAttribute('id')
            pourquoi_2.push(elem.getAttribute('id'))
            valeur_2.push(elem.value)
            var valeur = elem.value
            console.log(pourquoi);
          })
        }else if (i==3) {
          console.log(bloc_pourquoi.childNodes)
          bloc_pourquoi.childNodes.forEach((elem)=>{
            console.log(elem.getAttribute('id'),elem.value);
            var id = elem.getAttribute('id')
            pourquoi_3.push(elem.getAttribute('id'))
            valeur_3.push(elem.value)
            var valeur = elem.value
            console.log(pourquoi);
          })
        }else if (i==4) {
          console.log(bloc_pourquoi.childNodes)
          bloc_pourquoi.childNodes.forEach((elem)=>{
            console.log(elem.getAttribute('id'),elem.value);
            var id = elem.getAttribute('id')
            pourquoi_4.push(elem.getAttribute('id'))
            valeur_4.push(elem.value)
            var valeur = elem.value
            console.log('ontest',elem.value);
          })
        }else if (i==5) {
          console.log(bloc_pourquoi.childNodes)
          bloc_pourquoi.childNodes.forEach((elem)=>{
            console.log(elem.getAttribute('id'),elem.value);
            var id = elem.getAttribute('id')
            pourquoi_5.push(elem.getAttribute('id'))
            valeur_5.push(elem.value)
            var valeur = elem.value
            console.log(pourquoi);
          })
        }
      }

      $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/analyse_agent?reference=000012&n=1",
        data: {
          identifiant :identifiant,
          probleme :probleme,
          valeur_1 :valeur_1,
          valeur_2 :valeur_2,
          //pourquoi_3 :pourquoi_3,
          valeur_3 :valeur_3,
          //pourquoi_4 :pourquoi_4,
          valeur_4 :valeur_4,
          //pourquoi_5 :pourquoi_5,
          valeur_5 :valeur_5,
          async:false
        }
      })
      //e.preventDefault()

})


var i = 1;
cre_bloc(enregistrement_cause, i);
cre_boutton(enregistrement_cause);

form = document.getElementById('form_action')


// Accédez à l'élément form …
var bouton_form = document.getElementById("bouton_form");



let xhr = new XMLHttpRequest();

let json = JSON.stringify({
  "name": "John",
  "surname": "Smith"
});
// … et prenez en charge l'événement submit.
/*bouton_form.addEventListener("click", function (event) {
  event.preventDefault();
  console.log("Hello!");
  sendData();
 
});*/