clean:
	rm -rf tweets.jsonl tweets.rdf

tweets.jsonl:
	./bin/twarc search '#nzpol' > tweets.jsonl

tweets.rdf:
	./bin/python convert.py

import:
	./import

upload:
	./bin/python upload.py

.PHONY: import clean
