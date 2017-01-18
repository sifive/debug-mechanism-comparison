HTML=index.html
HTML+=feed-implementation.html
HTML+=terminology.html
HTML+=poll.html
HTML+=poll-results/results.html

all:	$(HTML)

poll-results/results.txt:	poll-results/summarize.py poll-results/results.csv
	cd poll-results; ./summarize.py > results.txt; cd ..

%.html:	%.txt
	asciidoctor $<

clean:
	rm -f $(HTML)
