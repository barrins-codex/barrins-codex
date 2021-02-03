function cardElement (element) {
	return `<li>${element.count} <span class="card" scryfallId="${element.id}" data-tippy-content="
		<div class='card-container'>
			<img data-src='https://api.scryfall.com/cards/${element.id}?format=image' src='https://api.scryfall.com/cards/${element.id}?format=image' class='card-image'>
		</div>" >${element.name}</span></li>`
}

function wrapText (text, maxlen) {
	if (!text) { return "(N/A)" }

	if (text.length > maxlen) {
		return text.substr(0, maxlen - 3) + "..."
	}
	return text
}

function setName (data) {
	document.getElementById("deck-name").textContent = wrapText(
		data.name || "(No Name)",
		50
	)
}

function setHeader (data) {
	header_lines = []
	if (data.player || data.author) {
		header_lines.push(wrapText(data.player || data.author, 40))
	}
	document.getElementById("deck-header").innerHTML = header_lines.join("<br/>")
}

function setFooter (data) {
	footer_lines = []
	if (data.date) {
		footer_lines.push(wrapText("Decklist posted on " + data.date, 40))
	}
	document.getElementById("deck-footer").innerHTML = footer_lines.join("<br/>")
}

function setCommanders (data) {
	var cards = []
	data.command.cards.forEach((value, index) => {
		cards.push(cardElement(value, index))
	})
	document.getElementById("commanders").innerHTML = cards.join("\n")
}

function setLibrary (data) {
	var library = document.getElementById('library-container')
	for (const section of data.library.cards) {
		if (section.count != 0) {
			// Create container for current section
			var divSection = document.createElement("div")
			// Create title for current section
			var title =  document.createElement("h4");
			title.innerHTML = `— ${section.type} (${section.count}) —`
			divSection.appendChild(title)
			// Create cardlist for current section
			var cardlist = document.createElement("ul")
			var cards = new Array()
			section.cards.forEach((value, index) => {
				cards.push(cardElement(value))
			})
			cardlist.innerHTML = cards.join("\n")
			divSection.appendChild(cardlist)
			// Push section into decklist
			library.appendChild(divSection)
		}
	}
}

function displayDeck (data) {
	setName(data)
	setHeader(data)
	setCommanders(data)
	setLibrary(data)
	setFooter(data)
}
