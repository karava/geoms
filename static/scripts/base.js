/* Close dropdown and navbar on mobile in header */

const dropdownCloseButtons = document.querySelectorAll(
  ".mobile-dropdown-close"
);

dropdownCloseButtons.forEach((element) => {
  element.addEventListener("click", function () {
    const dropdownToggleElements =
      this.parentElement.parentElement.parentElement.querySelectorAll(
        ".dropdown-toggle"
      );
    dropdownToggleElements.forEach((dropdownToggleElement) => {
      dropdownToggleElement.click();
    });
  });
});

const navbarCloseButtons = document.querySelectorAll(
  ".dropdown-menu .navbar-toggler"
);

navbarCloseButtons.forEach((element) => {
  element.addEventListener("click", function () {
    const dropdownToggleElements =
      this.parentElement.parentElement.parentElement.querySelectorAll(
        ".dropdown-toggle"
      );
    dropdownToggleElements.forEach((dropdownToggleElement) => {
      dropdownToggleElement.click();
    });
  });
});

/* Search panel handler */

const searchPanelElement = document.querySelector(".search-panel");

const searchPanelToggleElements = document.querySelectorAll(
  ".search-panel-toggle"
);

searchPanelToggleElements.forEach((element) => {
  element.addEventListener("click", function () {
    searchPanelElement.classList.add("show");
  });
});

const searchPanelCloseButton = document.querySelector(".search-panel-close");

searchPanelCloseButton.addEventListener("click", function () {
  searchPanelElement.classList.remove("show");
});

const menuTogglerElement = document.querySelector(".menu-toggler");

menuTogglerElement.addEventListener("click", function () {
  searchPanelElement.classList.remove("show");
});

const input = document.querySelector('input');
const resultsList = document.querySelector('#search-list');

input.addEventListener('keyup', async function(event) {
  const query = input.value.trim();
  if (!query) {
    resultsList.innerHTML = '';
    return;
  }

  const response = await fetch(`/search/?q=${encodeURIComponent(query)}`);
  const data = await response.json();

  // Clear old results
  resultsList.innerHTML = '';

  data.forEach(item => {
    const li = document.createElement('li');
    li.innerHTML = `<a href="${item.url}" target="_blank" style="text-decoration: none;">${item.title}</a>`;
    resultsList.appendChild(li);
  })
})

// faq content handler

const faqItemHeaderButtons = document.querySelectorAll(
  ".faq-item .faq-item-header"
);

// faqItemHeaderButtons.forEach((element) => {
//   element.addEventListener("click", function () {
//     element.parentElement.classList.toggle("opened");
//   });
// });

// base.js
function scrollToIframe() {
  var iframe = document.getElementById("myIframe");
  if (iframe) {
    iframe.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}