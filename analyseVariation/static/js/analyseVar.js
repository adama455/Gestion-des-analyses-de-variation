const section2=document.getElementById('section2');
const section3=document.getElementById('section3');
const definirAction=document.getElementById('definir-action');
const ajoutAnalyse=document.getElementById('add-analyse');

const divPourquoi=document.getElementById('div-pourquoi');
const pourquoi=document.getElementById('pourquoi');
const pourquoiSuivant=document.getElementById('pourquoi-suivant');
const pourquoi1=document.getElementById('pourquoi1');



ajoutAnalyse.addEventListener('click', () => {
    section2.classList.toggle('show2');
})

definirAction.addEventListener('click', () => {
    section3.classList.toggle('show3');
})

pourquoi.addEventListener('click', () => {
    const input = document.createElement('input');
    input.name = ' pourquoi1';
    input.className='my-2'
    input.classList.add("col-12")
    input.type="text"
    pourquoi1.appendChild(input)
});

pourquoiSuivant.addEventListener('click', ()=> {
    let i = 1;
    alert('Please enter')
    // divPourquoi.innerHTML += `
    //     <div class='row pourquoi mb-2 d-flex align-items-center'>
    //         <label for='pourquoi1' class='col-3'>Pourquoi1</label>
        
    //         <div class="col-8" id="pourquoi2">
    //             <input type="text" name="pourquoi1" id="pourquoi2" class="col-12">
    //         </div>
    //         <div class="icon-add col-1 d-flex justify-content-end">
    //             <i class="fa-solid fa-circle-plus fs-4" style="cursor: pointer;" id="pourquoi2"></i>
    //         </div>
    //     </div> 

    // `
    i++;

    
});









