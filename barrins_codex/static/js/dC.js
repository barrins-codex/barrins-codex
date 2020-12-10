function dC(name) {
	get_card_image(name);
	document.getElementById("card-modal").style.display = "block";
}

function hC(name) {
	if (window.matchMedia("(hover: none)").matches) {
		return
	}
	get_card_image(name);
	document.getElementById("card-hover").style.display = "block";
}

function oC() {
	document.getElementById("card-hover").style.display = "none";
}
