HTML=index.html
HTML+=feed-implementation.html
HTML+=terminology.html

all:	$(HTML)

%.html:	%.txt
	asciidoctor $<

clean:
	rm -f $(HTML)
