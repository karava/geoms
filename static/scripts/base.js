/* Close dropdown and navbar on mobile in header */

const dropdownCloseButtons = document.querySelectorAll(
  ".mobile-dropdown-close"
);

dropdownCloseButtons.forEach(element => {
  element.addEventListener("click", function () {
    this.parentElement.parentElement.parentElement
      .querySelector(".dropdown-toggle")
      .click();
  });
});

const navbarCloseButtons = document.querySelectorAll(
  ".dropdown-menu .navbar-toggler"
);

navbarCloseButtons.forEach(element => {
  element.addEventListener("click", function () {
    this.parentElement.parentElement.parentElement
      .querySelector(".dropdown-toggle")
      .click();
  });
});
