$(document).ready(function () {
    preloaderFadeOutTime = 100;

    function hidePreloader() {
        var preloader = $('.spinner-wrapper');
        preloader.fadeOut(preloaderFadeOutTime);
    }
    hidePreloader();
}); 