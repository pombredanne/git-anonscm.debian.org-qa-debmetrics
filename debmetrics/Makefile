MANIFESTS = $(wildcard manifests/*.manifest)
ORM_MODULES = $(patsubst manifests/%.manifest,models/%.py,$(MANIFESTS))

models/%.py: manifests/%.manifest
	./manifest2orm.py $< > $@

all: $(ORM_MODULES)
