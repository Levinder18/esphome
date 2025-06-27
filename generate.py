import os
import yaml
import re
from jinja2 import Environment, FileSystemLoader

# --- Load components.yaml ---
with open("components.yaml") as f:
    config = yaml.safe_load(f)

# --- Setup Jinja2 environment ---
TEMPLATE_DIR = "templates"
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
BASE_OUTPUT_DIR = "components"
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
