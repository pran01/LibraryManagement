let registerBtn = document.querySelector(".register-member-btn");
let registerName = document.querySelector(".register-name");
let registerEmail = document.querySelector(".register-email");
let registerAdult = document.querySelector(".register-adult");
let registerAddress = document.querySelector(".register-address");
let memberMobile1 = document.querySelector(".member-mobile-1");
let memberMobile2 = document.querySelector(".member-mobile-2");

registerBtn.addEventListener("click", () => {
    let registerDetails = {
      "name": registerName.value,
      "email": registerEmail.value,
      "isAdult": registerAdult.checked,
      "address": registerAddress.value,
      "mobile": [],
    };
    if(memberMobile1.value)
    registerDetails.mobile.push(memberMobile1.value);
    if(memberMobile2.value)
    registerDetails.mobile.push(memberMobile2.value);
    console.log(registerDetails);
    fetch(`${window.origin}/register-member`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(registerDetails),
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
        console.log(data)
        alert("Member Registered");
      });
    });
  });

  