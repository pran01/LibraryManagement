let booksTable=document.querySelector(".books-table");
let filterContainer=document.querySelector(".filter-container");
let filterBtn=document.querySelector(".filter-btn");

let response = fetch(`${window.origin}/show-books/show`);
response.then(function (response) {
    response.json().then(function (data) {
        booksTable.innerHTML=`<tr>
        <th>ID</th>
        <th>Name</th>
        <th>Author</th>
        <th>Genres</th>
      </tr>`
    for(book of data["books"]){
        booksTable.innerHTML+=`<tr>
        <td>${book.id}</td>
        <td>${book.name}</td>
        <td>${book.author}</td>
        <td>${book.genres}</td>
        </tr>`
    }
    filterContainer.innerHTML=`<h2>Authors</h2>`
    for(author of data["authors"]){
        filterContainer.innerHTML+=`${author} <input type="checkbox" name="authors" value="${author}" /><br />`
    }

    filterContainer.innerHTML+=`<h2>Genres</h2>`
    for(genre of data["genres"]){
        filterContainer.innerHTML+=`${genre} <input type="checkbox" name="genres" value="${genre}" /><br />`
    }
    });
});

filterBtn.addEventListener("click",()=>{
    checkAuthors=document.getElementsByName("authors");
    filteredAuthors=[];
    checkGenres=document.getElementsByName("genres");
    filteredGenres=[];
    for(author of checkAuthors){
        if(author.checked)
        filteredAuthors.push(author.value);
    }
    for(genre of checkGenres){
        if(genre.checked)
        filteredGenres.push(genre.value);
    }
    let filterDetails={"authors":filteredAuthors,"genres":filteredGenres};
    fetch(`${window.origin}/filter-books`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(filterDetails),
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
            booksTable.innerHTML=`<tr>
            <th>id</th>
            <th>Name</th>
            <th>Author</th>
            <th>Genres</th>
          </tr>`;
        for(book of data["books"]){
            booksTable.innerHTML+=`<tr>
            <td>${book.id}</td>
            <td>${book.name}</td>
            <td>${book.author}</td>
            <td>${book.genres}</td>
            </tr>`
        }
        });
      });
})
