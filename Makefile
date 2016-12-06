HTML=debug-mechanism-comparison.html

all:	$(HTML)

%.html:	%.txt
	asciidoctor $<

clean:
	rm -f $(HTML)
