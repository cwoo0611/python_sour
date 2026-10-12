// 엘리먼트(요소) 얻기
const code = document.querySelector("#code");
const sang = document.querySelector("#sang");
const su = document.querySelector("#su");
const dan = document.querySelector("#dan");

const msg = document.querySelector("#msg");
const tbody = document.querySelector("#tbody");

const btnAdd = document.querySelector("#btnAdd");
const btnUpdate = document.querySelector("#btnUpdate");
const btnDelete = document.querySelector("#btnDelete");
const btnReload = document.querySelector("#btnReload");

function setMsg(text){
    msg.textContent = text;
}

// 입력 폼 초기화
function clearForm(){
    code.value = "";
    sang.value = "";
    su.value = "";
    dan.value = "";

    code.focus();
}

// 전체 자료 읽기 - 시작시, 추가후 실행
async function loadAll(){
    const res = await fetch("/api/sangdata");
    const result_datas = await res.json();
    //console.log(datas);
    //alert(datas);

    tbody.innerHTML = "";

    result_datas.datas.forEach(r => {
        const tr = document.createElement("tr");
        tr.innerHTML = "<td>" + r.code + "</td>" + 
            "<td>" + r.sang + "</td>" +
            "<td>" + r.su + "</td>" +
            "<td>" + r.dan + "</td>";
        tbody.appendChild(tr);
    });
    
    clearForm();
    setMsg("조회 완료");
}

window.onload = loadAll;
