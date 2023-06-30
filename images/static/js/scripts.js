// (async function() {
// })();

window.onload = function(e){
    console.log("JS for pinboard manager is ready");
    ThemeManagement();
    LabelsManagement();
}
function ThemeManagement(){
    const ts = document.getElementById('theme-selector');
    ts.addEventListener('click', function(){
        if (ts.checked) {
            document.body.classList.add('dark');
        } else {
            document.body.classList.remove('dark');
        }
    });
}

function LabelsManagement(){
    const ls = document.getElementById('label-selector');
    const listLabels = document.querySelectorAll('.image-label');

    ls.addEventListener('click', function(){
        if (ls.checked) {
            listLabels.forEach(l => l.classList.remove('hidden'));
        } else {
            listLabels.forEach(l => l.classList.add('hidden'));
        }
    });
}
