MANIFESTS = $(wildcard manifests/*.manifest)
ORM_MODULES = $(patsubst manifests/%.manifest,models/%.py,$(MANIFESTS))
MANIFEST_DIR = cat .debmetrics.ini | grep manifest | grep DIRECTORY | sed 's/.*\://' | sed -e 's/^ *//' -e 's/ *$$//'

models/%.py: $(shell $(MANIFEST_DIR))/%.manifest
	./manifest2orm.py $< > $@

all: $(ORM_MODULES)
