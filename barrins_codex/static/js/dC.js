function dC(scryfallId) {
	document.getElementById("card-image").src = "https://api.scryfall.com/cards/"+scryfallId+"?format=image";
	document.getElementById("card-modal").style.display = "block";
}

function hC(scryfallId) {
	if (window.matchMedia("(hover: none)").matches) {
		return
	}
	document.getElementById("card-hover-image").src = "https://api.scryfall.com/cards/"+scryfallId+"?format=image";
	document.getElementById("card-hover").style.display = "block";
}

function oC() {
	document.getElementById("card-hover").style.display = "none";
}
