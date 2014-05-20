METRICS_SOURCES_LIST := examples/manifests
METRIC_SOURCES := $(foreach metrics_file,$(METRICS_SOURCES_LIST),$(wildcard $(metrics_file)/*.manifest))

models/%.py: $(METRIC_SOURCES)
	python manifest2orm.py $^

all: models/%.py
