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

	var url = "https://api.scryfall.com/cards/search?q=" + clean(name) + "&is=firstprint";
	console.log(url);
	ajaxRequest.open("GET", url, true);
	ajaxRequest.send(null);
}

function clean(name) {
	return name.replace(","," ").replace("'"," ");
}

function process_card_json() {
	if (ajaxRequest.readyState == 4) { // The request is completed
		if (ajaxRequest.status == 200) { // HTTP OK
			json = JSON.parse(ajaxRequest.responseText);

			let uri = "";
			console.log(json);
			if (json.data[0].image_uris !== undefined) {
				uri = json.data[0].image_uris.normal;
			}
			if (json.data[0].card_faces !== undefined) {
				uri = json.data[0].card_faces[0].image_uris.normal;
			}

			document.getElementById("card-image").src = uri;
			document.getElementById("card-hover-image").src = uri;
		}
	}
}
