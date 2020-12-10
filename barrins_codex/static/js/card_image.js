var ajaxRequest;
function ajaxFunction() {

	try {
		// Opera 8.0+, Firefox, Safari
		ajaxRequest = new XMLHttpRequest();
	} catch (e) {
		// Internet Explorer Browsers
		try {
			ajaxRequest = new ActiveXObject("Msxml2.XMLHTTP");
		} catch (e) {
			try {
				ajaxRequest = new ActiveXObject("Microsoft.XMLHTTP");
			} catch (e) {
				// Something went wrong
				alert("Your browser broke!");
				return false;
			}
		}
	}
}

function get_card_image(name) {
	ajaxFunction();

	// Here processRequest() is the callback function.
	ajaxRequest.onreadystatechange = process_card_json;

	var url = "https://api.scryfall.com/cards/named?fuzzy=" + escape(name);

	ajaxRequest.open("GET", url, true);
	ajaxRequest.send(null);
}

function process_card_json() {
	if (ajaxRequest.readyState == 4) { // The request is completed
		if (ajaxRequest.status == 200) { // HTTP OK
			json = JSON.parse(ajaxRequest.responseText);
			document.getElementById("card-image").src = json.image_uris.normal;
			document.getElementById("card-hover-image").src = json.image_uris.normal;
		}
	}
}
