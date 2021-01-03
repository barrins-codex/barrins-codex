document.querySelectorAll('img.svg').forEach(function(img){
	var imgID = img.id;
	var imgClass = img.className;
	var imgURL = img.src;
	var img_width = img.offsetWidth;
	var img_height = img.offsetHeight;

	fetch(imgURL).then(function(response) {
		return response.text();
	}).then(function(text){
		// Create a parser
		var parser = new DOMParser();
		var xmlDoc = parser.parseFromString(text, "image/svg+xml");
		// Get the SVG tag, ignore the rest
		var svg = xmlDoc.getElementsByTagName('svg')[0];
		// Add replaced image's ID to the new SVG
		if(typeof imgID !== 'undefined') {
			svg.setAttribute('id', imgID);
		}
		// Add replaced image's classes to the new SVG
		if(typeof imgClass !== 'undefined') {
			svg.setAttribute('class', imgClass);
		}
		// Remove any invalid XML tags as per http://validator.w3.org
		svg.removeAttribute('xmlns:a');
		// Check if the viewport is set, if the viewport is not set the SVG wont't scale.
		svg.setAttribute('viewBox', '0 0 ' + svg.getAttribute('height') + ' ' + svg.getAttribute('width'));
		svg.setAttribute("height", 550*svg.getAttribute('height')/svg.getAttribute('width'));
		svg.setAttribute("width", 550);
		svg.setAttribute("preserveAspectRatio", "xMidYMid meet")
		// Replace image with new SVG
		img.parentNode.replaceChild(svg, img);
	});
});
