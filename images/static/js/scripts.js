// (async function() {
// })();

window.onload = function(e){
    console.log("JS for pinboard manager is ready");
    ThemeManagement();
    LabelsManagement();
    ThumbnailsSizeManagement();
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
function ThumbnailsSizeManagement(){
    const sm = document.getElementById('th-size-sm');
    const md = document.getElementById('th-size-md');
    const lg = document.getElementById('th-size-lg');
    const thList = document.getElementById('thumbnails-list');

    sm.addEventListener('click', function(){
        thList.classList.add("size-sm");
        thList.classList.remove("size-md");
        thList.classList.remove("size-lg");
    });
    md.addEventListener('click', function(){
        thList.classList.remove("size-sm");
        thList.classList.add("size-md");
        thList.classList.remove("size-lg");
    });
    lg.addEventListener('click', function(){
        thList.classList.remove("size-sm");
        thList.classList.remove("size-md");
        thList.classList.add("size-lg");
    });
    
}
