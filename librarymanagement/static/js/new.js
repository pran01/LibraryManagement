let issueBookId=document.querySelector(".issue-book-id");
let issueMemberId=document.querySelector(".issue-memberid");
let returnBookId=document.querySelector(".return-book-id");
let issueBookNo=document.querySelector("#issueBookNo");
let returnBookNo=document.querySelector("#returnBookNo");
let addedBookIds=document.querySelector(".add-book-id");
let firstBookId=document.querySelector(".bookid-1");
let submitIssue=document.querySelector(".submit-issue");


issueBookNo.addEventListener("change",(evt)=>{
    addedBookIds.innerHTML="";
    for(let i=0;i<evt.target.value;i++){
        addedBookIds.innerHTML+=`<label>BookId</label>
        <input class=book-id${i+1}></input><br />`;
    }
})
submitIssue.addEventListener("click",()=>{
    let bookIdJson={"memberid": `${issueMemberId.value}` ,"bookid":[]};
    for(let i=0;i<issueBookNo.value;i++){
        bookIdJson.bookid.push(document.querySelector(`.book-id${i+1}`).value);
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
})

// returnBookNo.addEventListener("change",(evt)=>{
//     returnBookId.innerHTML="";
//         for(let i=0;i<evt.target.value;i++){
//             returnBookId.innerHTML+=`<label>Book ID</label>
//             <input type="number" placeholder="For Book ${i+1}" id="returnBookID${i+1}">`
//         }
// })
