if (localStorage.theme === 'dark' || (!'theme' in localStorage && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.querySelector('html').classList.add('dark')
} else if (localStorage.theme === 'dark') {
    document.querySelector('html').classList.add('dark')
}


setTimeout(function(){
    document.getElementById('preloader').style.display = 'none';
   }, 5);


function toggleTheme() {
    let htmlClasses = document.querySelector('html').classList;
    if(localStorage.theme == 'dark') {
        htmlClasses.remove('dark');
        localStorage.theme = 'light';
    } else {
        htmlClasses.add('dark');
        localStorage.theme = 'dark';
    }
  }