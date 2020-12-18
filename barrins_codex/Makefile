PYTHON=python
PRINTINGS=AllPrintings.json.gz
SETLIST=SetList.json.gz

.PHONY: clean

all: models

$(PRINTINGS):
	# wget -N https://mtgjson.com/json/$(JSON)
	# curl --remote-time -o ${JSON} https://mtgjson.com/api/v5/$(JSON)
	## What we really want here is to use remote timestamp if file exists, else
	## use the current timestamp.
	curl -o ${PRINTINGS} https://mtgjson.com/api/v5/$(PRINTINGS)

$(SETLIST):
	# wget -N https://mtgjson.com/json/$(JSON)
	# curl --remote-time -o ${JSON} https://mtgjson.com/api/v5/$(JSON)
	## What we really want here is to use remote timestamp if file exists, else
	## use the current timestamp.
	curl -o ${SETLIST} https://mtgjson.com/api/v5/$(SETLIST)

download: $(PRINTINGS) $(SETLIST)

library: $(PRINTINGS) $(SETLIST)
	$(PYTHON) build_library.py && touch ./static/json

clean:
	rm $(PRINTINGS)
	rm $(SETLIST)
