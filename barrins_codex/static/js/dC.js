function dC(url) {
	document.getElementById("card-image").src = name;
	document.getElementById("card-modal").style.display = "block";
}

function hC(url) {
	if (window.matchMedia("(hover: none)").matches) {
		return
	}
	document.getElementById("card-hover-image").src = 'url;
	document.getElementById("card-hover").style.display = "block";
}

function oC() {
	document.getElementById("card-hover").style.display = "none";
}
