
FILE ?= main.yaml.j2
TEMPLATES ?= ""
OUTPUT ?= ./output/final.yaml

.PHONY: generate-components install-component-generator

generate-components:
	. .venv/bin/activate && python3 componentGenerator/generate.py -f componentGenerator/$(FILE) -t $(TEMPLATES) -o $(OUTPUT)

generate-components-application:
	. .venv/bin/activate && python3 componentGenerator/generate.py -f applications/$(APPLICATION)/$(FILE) -t applications/$(APPLICATION)/components -o applications/$(APPLICATION)/output/final.yaml

install-component-generator:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r componentGenerator/requirements.txt
