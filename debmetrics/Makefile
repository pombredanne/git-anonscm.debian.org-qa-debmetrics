MANIFEST_DIR = cat .debmetrics.ini | grep manifest | grep DIRECTORY | sed 's/.*\://' | sed -e 's/^ *//' -e 's/ *$$//'
MANIFESTS = $(wildcard $(shell $(MANIFEST_DIR))/*.manifest)
ORM_MODULES = $(patsubst $(shell $(MANIFEST_DIR))/%.manifest,models/%.py,$(MANIFESTS))

models/%.py: $(shell $(MANIFEST_DIR))/%.manifest
	./manifest2orm.py $< > $@

templates/index.html: $(MANIFESTS)
	./manifest2index.py $^ > $@

all: $(ORM_MODULES) templates/index.html
