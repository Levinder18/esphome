
import os
import yaml
import re
import argparse
from jinja2 import Environment, FileSystemLoader


# --- Parse arguments ---

parser = argparse.ArgumentParser(description="Generate component files from templates.")
parser.add_argument("-f", "--file", required=True, help="Path to the components YAML file.")
parser.add_argument("-t", "--templates", default="componentGenerator/templates", help="Path to the templates directory (default: componentGenerator/templates)")
parser.add_argument("-o", "--output", default="components", help="Path to the output directory (default: components)")
args = parser.parse_args()

# --- Load the specified components YAML file ---
with open(args.file) as f:
    config = yaml.safe_load(f)


# --- Setup Jinja2 environment ---
TEMPLATE_DIR = args.templates
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# --- Dynamically build template registry ---
registry = {}  # { type: { section: template } }

for filename in os.listdir(TEMPLATE_DIR):
    match = re.match(r"(?P<type>\w+)_(?P<section>\w+)\.yaml\.j2$", filename)
    if match:
        type_ = match.group("type")
        section = match.group("section")
        registry.setdefault(type_, {})[section] = env.get_template(filename)


# --- Output ---
BASE_OUTPUT_DIR = args.output
os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)

for comp in config["components"]:
    comp_id = comp["id"]
    comp_type = comp["type"]
    comp_dir = os.path.join(BASE_OUTPUT_DIR, comp_id)
    os.makedirs(comp_dir, exist_ok=True)

    templates = registry.get(comp_type, {})

    for section, template in templates.items():
        if section == "interval" and "interval" not in comp:
            continue
        output_path = os.path.join(comp_dir, f"{section}.yaml")
        with open(output_path, "w") as f:
            f.write(template.render(**comp))
        print(f"[✓] Generated {section} for {comp_id}")
