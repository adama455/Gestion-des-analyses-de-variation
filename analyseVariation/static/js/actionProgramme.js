const tbody = document.getElementById("corps");
const plus = document.getElementById("btn-plus");
var plus_lines;
var j = 1;
var k = 1;
var l = 1;
var nb = 1;


function td_input(parent, id_input) {
  let nbr = tbody.childNodes.length;
  td = document.createElement("td");
  td.className = "border";
  td.style = "padding: 0 !important;margin: 0 !important";
  input = document.createElement("input");
  input.className = "border-0 tx-center w-100 fs-5 p-1";
  input.name = "action";
  input.value = "programme";
  input.setAttribute("id", `line_${nbr}_input_${id_input}`);
  td.appendChild(input);
  parent.appendChild(td);
}

function cre_tr(parent, id_input) {
  tr = document.createElement("tr");
  tr.setAttribute("id", ``);
  tr.className = "line";
  tr.style = "padding: 0 !important;margin: 0 !important";
  td = document.createElement("td");
  td.className = "border";
  td.style = "padding: 0 !important;margin: 0 !important";
  input = document.createElement("input");
  input.className = "border-0 tx-center w-100 fs-5 p-1";
  input.name = "action";
  input.setAttribute("id", `${id_input}`);
  td.appendChild(input);
  tr.appendChild(td);
  parent.appendChild(tr);
}

function cre_table(parent) {
  console.log(tbody.childNodes.length);
  let nbr = tbody.childNodes.length;
  table = document.createElement("table");
  td2 = document.createElement("td");
  td2.className = "border col-3 p-0";
  t_b = document.createElement("tbody");
  t_b.className = "tbody2"
  tr = document.createElement("tr");
  tr.setAttribute("id", "");
  tr.className = "line";
  table.className = "col-12";
  tr.style = "padding: 0 !important;margin: 0 !important";
  td_input(tr, nb++); //td3
  // tr.appendChild(td5); //td5
  t_b.appendChild(tr);
  table.appendChild(t_b);
  td2.appendChild(table);
  parent.appendChild(td2);
}

function cre_td_plus(parent){
  let nbr = tbody.childNodes.length;
  td = document.createElement("td");
  td.className = "col-1";
  i = document.createElement("i");
  i.className = "fa-light fa-plus fs-3 mt-5 tx-danger btn-plus-tr";
  i.setAttribute("id", `btn-plus-tr_${nbr}`);
  i.style = "cursor:pointer";
  td.appendChild(i);
  parent.appendChild(td)
}

function table_tbody(parent) {
  let nbr = tbody.childNodes.length;
  trr = document.createElement("tr");
  trr.className = "";
  trr.setAttribute("id", `line_${nbr}`);
  td_input(trr,nb++) //td1
  cre_table(trr);  //td2
  cre_table(trr);  //td3
  cre_table(trr);  //td4
  cre_td_plus(trr); //td5
  console.log(trr);
  parent.appendChild(trr);
}

plus.addEventListener("click", (e) => {
  alert("Okk");
  table_tbody(tbody);
  plus_lines = document.querySelectorAll("i.btn-plus-tr");
  console.log(plus_lines.length);

  for (let element = 0; element < plus_lines.length; element++) {
    plus_lines[element].addEventListener("click", (e) => {
      
      td1 = e.target.parentNode.previousSibling;
      td2 = td1.previousSibling;
      td3 = td2.previousSibling;
      console.log(td2);

      td1_tbody = td1.children[0].children[0];
      td2_tbody = td2.children[0].children[0];
      td3_tbody = td3.children[0].children[0];
      console.log(td1_tbody);

      input_precdt1 = td1_tbody.children[0].children[0].children[0];
      id_input_precdt1 = input_precdt1.getAttribute("id");
      input_precdt2 = td2_tbody.children[0].children[0].children[0];
      id_input_precdt2 = input_precdt2.getAttribute("id");
      input_precdt3 = td3_tbody.children[0].children[0].children[0];
      id_input_precdt3 = input_precdt3.getAttribute("id");
      console.log(id_input_precdt1)

      cre_tr(td1_tbody, id_input_precdt1 + `${j++}`);
      cre_tr(td2_tbody, id_input_precdt2 + `${k++}`);
      cre_tr(td3_tbody, id_input_precdt3 + `${l++}`);

      alert("Okk");


    // td1 = e.target.parentNode.previousSibling.previousSibling;
      // td2 = td1.previousSibling.previousSibling;
      // td3 = td2.previousSibling;

      // td1_tbody = td1.children[0].children[0];
      // td2_tbody = td2.children[0].children[0];
      // td3_tbody = td3.children[0].children[0];
      // console.log(td1.childNodes.length - 1);

      // input_precdt1 = td1_tbody.children[0].children[0].children[0];
      // id_input_precdt1 = input_precdt1.getAttribute("id");
      // input_precdt2 = td2_tbody.children[0].children[0].children[0];
      // id_input_precdt2 = input_precdt2.getAttribute("id");
      // input_precdt3 = td3_tbody.children[0].children[0].children[0];
      // id_input_precdt3 = input_precdt3.getAttribute("id");
      // console.log(id_input_precdt2);

      // cre_tr(td1_tbody, id_input_precdt1 + `${j++}`);
      // cre_tr(td2_tbody, id_input_precdt2 + `${k++}`);
      // cre_tr(td3_tbody, id_input_precdt3 + `${l++}`);

    });
  }
});

