ifneq ("$(wildcard .debmetrics.local.ini)","")
CONFIG_FILE = .debmetrics.local.ini
else ifneq ("$(wildcard /etc/debmetrics/debmetrics.ini)","")
CONFIG_FILE = /etc/debmetrics/debmetrics.ini
else
$(error Couldn't find config file at ./.debmetrics.local.ini or /etc/debmetrics/debmetrics.ini) # Vim syntax highlighting fix '
endif

MANIFEST_DIR = cat $(CONFIG_FILE) | grep manifest | grep DIRECTORY | sed 's/.*\://' | sed -e 's/^ *//' -e 's/ *$$//'
MANIFESTS = $(wildcard $(shell $(MANIFEST_DIR))/*.manifest)
ORM_MODULES = $(patsubst $(shell $(MANIFEST_DIR))/%.manifest,debmetrics/models/%.py,$(MANIFESTS))

all: install-depends-stamp $(ORM_MODULES) templates/index.html create-all-stamp

install-depends-stamp: $(MANIFESTS)
ifneq ("$(wildcard /etc/debian-release)", "")
	./install_depends.py
else
	@echo "Skipping installing dependencies, because you are missing /etc/debian-release"
endif
	touch $@

debmetrics/models/%.py: $(shell $(MANIFEST_DIR))/%.manifest debmetrics/manifest2orm.py
	./debmetrics/manifest2orm.py $< > $@

templates/index.html: $(MANIFESTS)
	./debmetrics/manifest2index.py $^ > $@

create-all-stamp: $(MANIFESTS)
	python3 create_all.py
	touch $@
