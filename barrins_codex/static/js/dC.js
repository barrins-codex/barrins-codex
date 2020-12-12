function dC(name) {
	get_card_image(name, "card-image");
	document.getElementById("card-modal").style.display = "block";
}

function hC(name) {
	if (window.matchMedia("(hover: none)").matches) {
		return
	}
	get_card_image(name, "card-hover-image");
	document.getElementById("card-hover").style.display = "block";
}

function oC() {
	document.getElementById("card-hover").style.display = "none";
}

function sC(name, target) {
	console.log("Chargement de l'image : "+name);
	get_card_image(name, target, "small");
}
