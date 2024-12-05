let text = document.getElementById('text');
let gateRight = document.getElementById('gate-right');
let gateLeft = document.getElementById('gate-left');

window.addEventListener('scroll', ()=> {
    let value = window.scrollY;
    text.style.marginTop = value*2.5 + 'px';
    gateLeft.style.left = value*0.5 +'px';
    gateRight.style.left = value*-0.5 +'px';
});