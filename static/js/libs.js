let oldScrollY = 0;
const topmenu = document.getElementsByClassName("topmenu")[0];

window.onscroll = (e) => {
    const scrolled = document.documentElement.scrollTop;
    if (scrolled - oldScrollY > 0) topmenu.classList.add('relative');
    else topmenu.classList.remove('relative');

    oldScrollY = scrolled;
}
