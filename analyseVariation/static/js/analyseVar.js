const section2 = document.getElementById("section2");
const section3 = document.getElementById("section3");
const definirAction = document.getElementById("definir-action");
const ajoutAnalyse = document.getElementById("add-analyse");

const divPourquoi = document.getElementById("div-pourquoi");
const pourquoi = document.querySelectorAll("pourquois");
const pourquoiSuivant = document.getElementById("pourquoi-suivant");
var pourqw = document.querySelectorAll(".pourqw");

// const pourquoi1=document.getElementById('pourquoi1');
// var pourqw;

// console.log("pourquoi : ",pourquoi);

ajoutAnalyse.addEventListener("click", () => {
  section2.classList.toggle("show2");
});

definirAction.addEventListener("click", () => {
  section3.classList.toggle("show3");
});

// function creerPourquoi(){
//     const div = document.createElement('div')
//     div.className = 'row pourquoi mb-2 d-flex align-items-center'
//     const label = document.createElement('label')
//     label.className = 'col-3'
//     label.innerText="Pourquoi"
//     const divInput = document.createElement('div')
//     divInput.className = 'col-8'
//     const input = document.createElement('input')
//     input.className = 'col-12'
//     const divIcon = document.createElement('div')
//     divIcon.className = 'icon-add col-1 d-flex justify-content-end'
//     const icon = document.createElement('i')
//     icon.className='fa-solid fa-circle-plus fs-4'
//     icon.id ="pourquoi"

//     divInput.append(input)
//     divIcon.append(icon)
//     div.append(label, divInput, divIcon)
//     divPourquoi.append(div)
// }

pourquoiSuivant.addEventListener("click", () => {
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
});

// Pour le premier Pourquoi qui apparait par défaut:::::::::
pourquoi.forEach((element) => {
  element.addEventListener("click", (e) => {
    const prq = e.target.parentElement.parentElement.children[1];
    const input = document.createElement("input");
    input.name = "pourquoi2";
    input.className = "my-2";
    input.classList.add("col-12");
    input.type = "text";
    prq.appendChild(input);
  });
});
