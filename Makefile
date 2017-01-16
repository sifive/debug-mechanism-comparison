HTML=index.html
HTML+=feed-implementation.html
HTML+=terminology.html
HTML+=poll.html

all:	$(HTML)

%.html:	%.txt
	asciidoctor $<

clean:
	rm -f $(HTML)
