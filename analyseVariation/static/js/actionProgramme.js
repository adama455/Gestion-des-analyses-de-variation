const tbody = document.getElementById("corps");
const plus = document.getElementById("btn-plus");
var nl = tbody.childNodes.length + 1;

function cre_input(Class, id_input,Valeur) {
  input = document.createElement("input");
  input.className = Class;
  input.name = "action";
  input.value = Valeur;
  input.setAttribute("id", `${id_input}`);
  // parent.appendChild(input);
  return input;
}
function cre_td(item) {
  td = document.createElement("td");
  td.className = "border border-dark";
  td.style = "padding: 0 !important;margin: 0 !important";
  td.appendChild(item);
  return td;
}
function cre_td_plus(parent,id) {
  let nbr = tbody.childNodes.length;
  td = document.createElement("td");
  td.className ="col-1";
  console.log(parent.childNodes.length);
  i = document.createElement("i");
  i.className = "fa-light fa-plus fs-3 mt-5 tx-primary btn-plus-tr";
  i.setAttribute("id", id);
  i.style = "cursor:pointer";
  td.appendChild(i);
  parent.appendChild(td);
}
function td_Input(id,valeur) {
  return cre_td(cre_input("border-0 tx-center w-100 fs-5 p-1",id,valeur))
}

// plus.addEventListener("click", (e) => {
//   // alert("Okk");
//   let nl = tbody.childNodes.length + 1;
//   tr = document.createElement("tr");
//   tr.className = "";
//   tr.setAttribute("id", `line_${nl}`);
//   tr.appendChild(td_Input(`cause_${nl}`));
//   cre_td_plus(tr,`btn_plus_tr_${nl}`); //td5
//   console.log(tr.childNodes.length);
//   tbody.appendChild(tr)
//   plus_lines = document.querySelectorAll("i.btn-plus-tr");
//   console.log(plus_lines.length);

//   for (let element = 0; element < plus_lines.length; element++) {
//     let nac = tbody.childNodes.length;
//     let np = tbody.childNodes.length;
//     let ne = tbody.childNodes.length;
//     plus_lines[element].addEventListener("click", (e) => {
//       e.stopImmediatePropagation();
//       plus_ac = document.getElementById(`btn_plus_tr_${nl}`)
//       // console.log(plus_ac.parentNode);
//       tr = document.getElementById(`line_${nl}`)
//       console.log(tr.childNodes.length);
//       if(tr.childNodes.length <= 2){
//         console.log( e.target.parentNode.parentNode.childNodes.length );
//         let t = e.target.parentNode.parentNode.childNodes.length - 1
//         let v = e.target.parentNode.parentNode.childNodes.length - 1
//         let w = e.target.parentNode.parentNode.childNodes.length - 1
//         tr.insertBefore(td_Input(`cause_${nl}_action_${t}`), plus_ac.parentNode)
//         tr.insertBefore(td_Input(`cause_${nl}_porteur_${t}`), plus_ac.parentNode)
//         tr.insertBefore(td_Input(`cause_${nl}_echeance${t}`), plus_ac.parentNode)
//       }else{
//         td1 = e.target.parentNode.previousSibling.previousSibling.previousSibling;
//         let i = td1.childNodes.length + 1;
//         td2 = td1.nextSibling;
//         let j = td2.childNodes.length + 1;
//         td3 = td2.nextSibling;
//         let k = td3.childNodes.length + 1;
//         console.log(td2);
//         td1.appendChild( cre_input("border tx-center w-100 fs-5 p-1", `cause_${nl}_action_${i}`));
//         td2.appendChild( cre_input("border tx-center w-100 fs-5 p-1", `cause_${nl}_porteur_${j}`));
//         td3.appendChild( cre_input("border tx-center w-100 fs-5 p-1", `cause_${nl}_echeance_${k}`));
//       }
//       // alert("Okk");
//     });
//   }
// });


for (let index = 0; index <2; index++) {

  let nl = tbody.childNodes.length + 1;
  tr = document.createElement("tr");
  tr.className = "";
  tr.setAttribute("id", `line_${nl}`);
  tr.appendChild(td_Input(`cause_${nl}`,"Causes"));
  cre_td_plus(tr,`btn_plus_tr_${nl}`); //td5
  console.log(tr.childNodes.length);
  tbody.appendChild(tr)
  plus_lines = document.querySelectorAll("i.btn-plus-tr");
  console.log(plus_lines.length);

  for (let element = 0; element < plus_lines.length; element++) {
    let nac = tbody.childNodes.length;
    let np = tbody.childNodes.length;
    let ne = tbody.childNodes.length;
    plus_lines[element].addEventListener("click", (e) => {
      e.stopImmediatePropagation();
      plus_ac = document.getElementById(`btn_plus_tr_${nl}`)
      // console.log(plus_ac.parentNode);
      tr = document.getElementById(`line_${nl}`)
      console.log(tr.childNodes.length);
      if(tr.childNodes.length <= 2){
        console.log( e.target.parentNode.parentNode.childNodes.length );
        let t = e.target.parentNode.parentNode.childNodes.length - 1
        let v = e.target.parentNode.parentNode.childNodes.length - 1
        let w = e.target.parentNode.parentNode.childNodes.length - 1
        tr.insertBefore(td_Input(`cause_${nl}_action_${t}`, ""), plus_ac.parentNode)
        tr.insertBefore(td_Input(`cause_${nl}_porteur_${t}`, ""), plus_ac.parentNode)
        tr.insertBefore(td_Input(`cause_${nl}_echeance${t}`, ""), plus_ac.parentNode)
      }else{
        td1 = e.target.parentNode.previousSibling.previousSibling.previousSibling;
        let i = td1.childNodes.length + 1;
        td2 = td1.nextSibling;
        let j = td2.childNodes.length + 1;
        td3 = td2.nextSibling;
        let k = td3.childNodes.length + 1;
        console.log(td2);
        td1.appendChild( cre_input("border tx-center w-100 fs-5 p-1", `cause_${nl}_action_${i}`, ""));
        td2.appendChild( cre_input("border tx-center w-100 fs-5 p-1", `cause_${nl}_porteur_${j}`, ""));
        td3.appendChild( cre_input("border tx-center w-100 fs-5 p-1", `cause_${nl}_echeance_${k}`, ""));
      }
      // alert("Okk");
    });
  }
  
}

function ajax(method, data, url) {
  // var url = new URL(window.location.href);
  // var id = document.getElementById("identifiant_act").value;
  // console.log(id);
  // var reference = document.getElementById("reference_av_act").value;
  // var n = url.searchParams.get("n");
  // console.log(reference);
  // url = Url + "?reference=" + reference + "&n=" + n + "&id=" + id;
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

$(document).ready(function () {
  $("#action_programme").click(function (event) {
    var n = document.getElementById("corps").childNodes;
    // console.log(n);
    var ACTION = [];
    var actions = [];
    n.forEach((element) => { //lines
      console.log(element);
      // for (let j = 0; j < element.childNodes.length; j++) {  //colonnes
        var colonnes = [];
        for (let k = 0; k < element.children[1].childNodes.length; k++) {  
          console.log(element.childNodes[1].childNodes[0]);
          colonnes.push(element.children[0].childNodes[0].value);
          colonnes.push(element.children[1].childNodes[k].value);
          colonnes.push(element.children[2].childNodes[k].value);
          colonnes.push(element.children[3].childNodes[k].value);
          console.log(actions);
          colonnes.push('{');
        }
        actions.push(colonnes);
        actions.push('|');

      // }
    });
    ACTION.push(actions);
    console.log(ACTION);
    ajax(
      method= 'POST',
      data = ACTION.toString(),
      url= 'http://127.0.0.1:5000/action_programme'
    )
    // window.location.reload();
  });
});
