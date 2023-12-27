// content.js
window.onload = function () {
  let attachButton = document.querySelector(".attach-button-selector"); // 첨부하기 버튼의 실제 selector로 교체해야 합니다.
  if (attachButton) {
    let checkButton = document.createElement("button");
    checkButton.innerText = "Check";
    checkButton.addEventListener("click", function () {
      // 체크버튼을 클릭했을 때 수행할 동작을 여기에 작성합니다.
    });
    attachButton.parentNode.insertBefore(checkButton, attachButton.nextSibling);
  }
};

let attachButton = document.querySelector(".attach-button-selector");
console.log(attachButton); // 이 로그를 통해 attachButton이 제대로 찾아졌는지 확인할 수 있습니다.
