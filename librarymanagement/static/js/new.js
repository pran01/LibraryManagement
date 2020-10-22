let issueBookId = document.querySelector(".issue-book-id");
let issueMemberId = document.querySelector(".issue-memberid");
let returnBookId = document.querySelector(".return-book-id");
let returnMemberId = document.querySelector(".return-memberid");
let issueBookNo = document.querySelector("#issueBookNo");
let returnBookNo = document.querySelector("#returnBookNo");
let addedBookIds = document.querySelector(".add-book-id");
let firstBookId = document.querySelector(".bookid-1");
let submitIssue = document.querySelector(".submit-issue");
let getBooksBtn = document.querySelector(".get-book-details");
let issuedBooks = document.querySelector(".issued-books");
let submitReturn = document.querySelector(".submit-return");
let calculateFine = document.querySelector(".calculate-fine");
let showFine = document.querySelector(".show-fine");

calculateFine.setAttribute("hidden", "true");
submitReturn.setAttribute("hidden", "true");

issueBookNo.addEventListener("change", (evt) => {
  addedBookIds.innerHTML = "";
  for (let i = 0; i < evt.target.value; i++) {
    addedBookIds.innerHTML += `<label>BookId</label>
        <input class=book-id${i + 1}></input><br />`;
  }
});


submitIssue.addEventListener("click", () => {
  let bookIdJson = { memberid: `${issueMemberId.value}`, bookid: [] };
  for (let i = 0; i < issueBookNo.value; i++) {
    bookIdJson.bookid.push(document.querySelector(`.book-id${i + 1}`).value);
  }
  fetch(`${window.origin}/submit-issue`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(bookIdJson),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json",
    }),
  }).then(function (response) {
    if (response.status != 200) {
      console.log(`Response status not 200 : ${response.status}`);
      return;
    }
  });
});


getBooksBtn.addEventListener("click", () => {
  let member = { memberid: `${returnMemberId.value}` };
  fetch(`${window.origin}/get-book-details`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(member),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json",
    }),
  }).then(function (response) {
    if (response.status != 200) {
      console.log(`Response status not 200 : ${response.status}`);
      return;
    }
    response.json().then(function (data) {
      issuedBooks.innerHTML = `Member ID: ${data.memberid} <br />`;
      for (book of data.bookid)
        issuedBooks.innerHTML += `<input readonly value="${book.name} (id: ${book.id})" /> <input type="checkbox" name="checkBooks" value=${book.id} /><br />`;
      calculateFine.removeAttribute("hidden");
    });
  });
});


submitReturn.addEventListener("click",()=>{
  let choices=document.getElementsByName("checkBooks");
  let returnId={"bookid":[]}
  for(let i=0;i<choices.length;i++){
    if(choices[i].checked){
      value=choices[i].value;
      returnId.bookid.push(value);
    }
  }
  fetch(`${window.origin}/submit-return`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(returnId),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json",
    }),
  }).then(function (response) {
    if (response.status != 200) {
      console.log(`Response status not 200 : ${response.status}`);
      return;
    }
    response.json().then(function (data) {
      console.log(data);
    });
  });
})


calculateFine.addEventListener("click",()=>{
  let choices=document.getElementsByName("checkBooks");
  let returnId={"bookid":[]}
  for(let i=0;i<choices.length;i++){
    if(choices[i].checked){
      value=choices[i].value;
      returnId.bookid.push(value);
    }
  }
  fetch(`${window.origin}/calculate-fine`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(returnId),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json",
    }),
  }).then(function (response) {
    if (response.status != 200) {
      console.log(`Response status not 200 : ${response.status}`);
      return;
    }
    response.json().then(function (data) {
      showFine.innerHTML=`<h4> Fine: ${data.fine} </h4>`;
      submitReturn.removeAttribute("hidden");
    });
  });
})