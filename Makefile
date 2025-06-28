
FILE ?= componentGenerator/components.yaml
TEMPLATES ?= componentGenerator/templates
CUSTOM_TEMPLATES ?= componentGenerator/custom_templates
OUTPUT ?= components

.PHONY: generate-components install-component-generator

generate-components:
	. .venv/bin/activate && python3 componentGenerator/generate.py -f $(FILE) -t $(TEMPLATES) -c $(CUSTOM_TEMPLATES) -o $(OUTPUT)

generate-components-application:
	. .venv/bin/activate && python3 componentGenerator/generate.py -f applications/$(APPLICATION)/components.yaml -t $(TEMPLATES) -c $(CUSTOM_TEMPLATES) -o applications/$(APPLICATION)/components

install-component-generator:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r componentGenerator/requirements.txt
