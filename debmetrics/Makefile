METRICS_SOURCES_LIST := examples/manifests
METRIC_SOURCES := $(foreach metrics_file,$(METRICS_SOURCES_LIST),$(wildcard $(metrics_file)/*.manifest))
ORM_LIST := models
ORMS := $(foreach model,$(ORM_LIST),$(wildcard $(model)/*.py))

$(ORMS): $(METRIC_SOURCES)
	@echo $(ORMS)
	@echo $(METRIC_SOURCES)
	python manifest2orm.py $?

all: $(ORMS)
