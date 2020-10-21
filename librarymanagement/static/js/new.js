let issueBookId=document.querySelector(".issue-book-id");
let returnBookId=document.querySelector(".return-book-id");
let issueBookNo=document.querySelector("#issueBookNo");
let returnBookNo=document.querySelector("#returnBookNo");


issueBookNo.addEventListener("change",(evt)=>{
    issueBookId.innerHTML="";
        for(let i=0;i<evt.target.value;i++){
            issueBookId.innerHTML+=`{{ issueForm.bookId.label }} {{ issueForm.bookId() }}`
        }
})

returnBookNo.addEventListener("change",(evt)=>{
    returnBookId.innerHTML="";
        for(let i=0;i<evt.target.value;i++){
            returnBookId.innerHTML+=`<label>Book ID</label>
            <input type="number" placeholder="For Book ${i+1}" id="returnBookID${i+1}">`
        }
})
