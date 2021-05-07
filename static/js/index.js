$(document).ready(function () {
    preloaderFadeOutTime = 1000;

    function hidePreloader() {
        var preloader = $('.spinner-wrapper');
        preloader.fadeOut(preloaderFadeOutTime);
    }
    hidePreloader();
});

let searchText = [
    "How to sign raw bitcoin transaction",
    "Using trezor-firmware",
    "Switching from bootstrap to tailwind",
    "How to sign raw ethereum transaction",
    "Understanding Shamir Secret Sharing algorithm",
];

var generate = document.getElementById('searchBar');
generate.value = searchText[Math.floor(Math.random()*searchText.length)];
