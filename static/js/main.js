
let header = document.querySelector(".home-header");
let headerLogoImage = document.querySelector("img.home-header-logo");
topLogo = headerLogoImage.src;
scrolledLogo = headerLogoImage.getAttribute("scrolled-logo");

window.onscroll = () => {HeaderScrollChange()};

const HeaderScrollChange = () => {
    if (window.scrollY > 0) {
        header.classList.add("scrolled-header");
        headerLogoImage.src = scrolledLogo;
    } else {
        header.classList.remove("scrolled-header");
        headerLogoImage.src = topLogo;

    }
}
