var h = document.documentElement,
    b = document.body,
    st = "scrollTop",
    sh = "scrollHeight",
    progress = document.querySelector("#progress"),
    scroll;
var scrollpos = window.scrollY;
var header = document.getElementById("header");
var navcontent = document.getElementById("nav-content");
document.addEventListener("scroll", function () {
    scroll = (h[st] || b[st]) / ((h[sh] || b[sh]) - h.clientHeight) * 100;
    progress.style.setProperty("--scroll", scroll + "%");
    scrollpos = window.scrollY;
    if (scrollpos > 10) {
        header.classList.add("bg-white");
        header.classList.add("shadow-xl");
        navcontent.classList.remove("bg-gray-50");
        navcontent.classList.add("bg-white")
    } else {
        header.classList.remove("bg-white");
        header.classList.remove("shadow-xl");
        navcontent.classList.remove("bg-white");
        navcontent.classList.add("bg-gray-50")
    }
});

// const toggle = document.querySelector('#switch-toggle');
// const body = document.querySelector('html');
// function toggleTheme()
// {
// if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
//     document.documentElement.classList.add('dark')
//   } else {
//     document.documentElement.classList.remove('dark')
// }
// console.log(body);
//   }

// toggle.addEventListener('click', () => {

//     if (localStorage.theme === 'light') {
//         toggle.innerHTML = "<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='feather feather-sun'><circle cx='12' cy='12' r='5'></circle><line x1='12' y1='1' x2='12' y2='3'></line><line x1='12' y1='21' x2='12' y2='23'></line><line x1='4.22' y1='4.22' x2='5.64' y2='5.64'></line><line x1='18.36' y1='18.36' x2='19.78' y2='19.78'></line><line x1='1' y1='12' x2='3' y2='12'></line><line x1='21' y1='12' x2='23' y2='12'></line><line x1='4.22' y1='19.78' x2='5.64' y2='18.36'></line><line x1='18.36' y1='5.64' x2='19.78' y2='4.22'></line></svg>";
//         localStorage.theme = 'dark'
//     } else {
//         toggle.innerHTML = "<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='feather feather-moon'><path d='M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z'></path></svg>";
//         localStorage.theme = 'light'
//     }
//     toggleTheme();
// });
  