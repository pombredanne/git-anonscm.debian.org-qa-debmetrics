MANIFEST_DIR = cat .debmetrics.ini | grep manifest | grep DIRECTORY | sed 's/.*\://' | sed -e 's/^ *//' -e 's/ *$$//'
MANIFESTS = $(wildcard $(shell $(MANIFEST_DIR))/*.manifest)
ORM_MODULES = $(patsubst $(shell $(MANIFEST_DIR))/%.manifest,debmetrics/models/%.py,$(MANIFESTS))

all: install-depends-stamp $(ORM_MODULES) templates/index.html create-all-stamp

install-depends-stamp: $(MANIFESTS)
	./install_depends.py
	touch $@

debmetrics/models/%.py: $(shell $(MANIFEST_DIR))/%.manifest
	./debmetrics/manifest2orm.py $< > $@

templates/index.html: $(MANIFESTS)
	./debmetrics/manifest2index.py $^ > $@

create-all-stamp: $(MANIFESTS)
	python3 create_all.py
	touch $@
