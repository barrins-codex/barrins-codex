// Function from : https://www.quirksmode.org/dom/toc.html
var TOCstate = "none";

function showhideTOC() {
    TOCstate = (TOCstate == 'none') ? 'block' : 'none';
    var newText = (TOCstate == 'none') ? 'Afficher la table des matières' : 'Masquer la table des matières';
    var newClass = (TOCstate == 'none') ? 'toc-down' : 'toc-up';
    document.getElementById('contentheader').innerHTML = newText;
    document.getElementById('contentheader').className = newClass;
    document.getElementById('innertoc').lastChild.style.display = TOCstate;
}

(function createTOC() {
    var y = document.getElementById('put-toc');
    y.id = 'innertoc';
    var a = y.appendChild(document.createElement('span'));
    a.onclick = showhideTOC;
    a.id = 'contentheader';
    a.innerHTML = 'Masquer la table des matières';
    a.className = "toc-up";
    var z = y.appendChild(document.createElement('div'));
    z.onclick = showhideTOC;
    var toBeTOCced = document.querySelectorAll('h2[id],h3[id],h4[id],h5[id]');
    if (toBeTOCced.length < 2) return false;

    let start_h2 = 49, start_h3 = 65, start_h4 = 97;
    let h2 = start_h2, h3 = start_h3, h4 = start_h4;
    for (var i = 0; i < toBeTOCced.length; i++) {
        var tmp = document.createElement('a');
        tmp.innerHTML = toBeTOCced[i].textContent.trim();
        tmp.className = 'page text-reset';
        z.appendChild(tmp);
        if (toBeTOCced[i].nodeName == 'H2') {
            tmp.innerHTML = String.fromCharCode(h2) + " - " + tmp.innerHTML;
            h2 ++; h3 = start_h3; h4 = start_h4;
        }
        if (toBeTOCced[i].nodeName == 'H3') {
            tmp.innerHTML = String.fromCharCode(h2-1) + "." + String.fromCharCode(h3) + " - " + tmp.innerHTML;
            h3++; h4 = start_h4;
            tmp.className += ' indent';
        }
        if (toBeTOCced[i].nodeName == 'H4') {
            tmp.innerHTML = String.fromCharCode(h2-1) + "." + String.fromCharCode(h3-1) + "." + String.fromCharCode(h4) + " - " + tmp.innerHTML;
            h4++;
            tmp.className += ' extraindent';
        }
        if (toBeTOCced[i].nodeName == 'H5') {
            tmp.className += ' extraextraindent';
        }
        var headerId = toBeTOCced[i].id || 'link' + i;
        tmp.href = '#' + headerId;
        toBeTOCced[i].id = headerId;
        tmp.after(document.createElement("br"));
    }

    return y;
})();

showhideTOC();
