HTML=index.html

all:	$(HTML)

%.html:	%.txt
	asciidoctor $<

clean:
	rm -f $(HTML)
