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

function get_card_image(name, target, size="normal") {
	// Initiate AJAX function
	ajaxFunction();

	// Here processRequest() is the callback function.
	ajaxRequest.onreadystatechange = function () {
		if (ajaxRequest.readyState == 4) { // The request is completed
			if (ajaxRequest.status == 200) { // HTTP OK
				json = JSON.parse(ajaxRequest.responseText);
				if (size === "normal") {
					document.getElementById(target).src = json.image_uris.normal;
				}else if (size === "small") {
					document.getElementById(target).src = json.image_uris.small;
				}
			}
		}
	}

	var url = "https://api.scryfall.com/cards/named?fuzzy=" + escape(name);

	ajaxRequest.open("GET", url, true);
	ajaxRequest.send(null);
}
