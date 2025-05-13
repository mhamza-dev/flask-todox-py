document.addEventListener("DOMContentLoaded", function () {
  const flashMessages = document.querySelectorAll(".flash-messages");
  flashMessages.forEach((flashMessage) => {
    setTimeout(() => {
      flashMessage.classList.add("fade");
    }, 3000);
  });
});
