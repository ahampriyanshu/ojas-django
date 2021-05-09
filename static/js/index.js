$(document).ready(function () {
    preloaderFadeOutTime = 500;
    function hidePreloader() {
        var preloader = $('.preloader');
        preloader.fadeOut(preloaderFadeOutTime);
    }
    hidePreloader();
}); 

$('.captcha').click(function () {
    $.getJSON("/captcha/refresh/", function (result) {
        $('.captcha').attr('src', result['image_url']);
        $('#id_captcha_0').val(result['key'])
    });
});

const toggle = document.querySelector('.toggleSwitch');
toggle.addEventListener('click', () => {
    if (localStorage.darkMode === true) {
        localStorage.darkMode = false
    } else {
        localStorage.darkMode = true
    }
});