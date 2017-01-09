HTML=index.html
HTML+=feed-implementation.html

all:	$(HTML)

%.html:	%.txt
	asciidoctor $<

clean:
	rm -f $(HTML)
