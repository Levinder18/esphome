import os
import yaml
import re
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# --- Argument parsing ---
parser = argparse.ArgumentParser(description="Generate component files from templates.")
parser.add_argument("-f", "--file", required=True, help="Path to the components YAML file.")
parser.add_argument("-t", "--templates", default="componentGenerator/templates", help="Path to the templates directory (default: componentGenerator/templates)")
parser.add_argument("-c", "--custom-templates", default="componentGenerator/custom_templates", help="Path to the custom templates directory (default: componentGenerator/custom_templates)")
parser.add_argument("-o", "--output", default="components", help="Path to the output directory (default: components)")

def to_nice_yaml(value, indent=2, explicit_end=True):
    out = yaml.dump(value, indent=indent, default_flow_style=False, sort_keys=False, explicit_end=False)
    return out.strip().replace('...', '')  # Remove doc end

def main():
    args = parser.parse_args()

    base_output_dir = args.output
    template_dir = args.templates
    custom_template_dir = args.custom_templates

    os.makedirs(base_output_dir, exist_ok=True)
    env = Environment(loader=FileSystemLoader([template_dir, custom_template_dir]))
    env.filters['to_nice_yaml'] = to_nice_yaml

    with open(args.file) as f:
        config = yaml.safe_load(f)

    defaults = config.get("defaults", {})
    components = [apply_inheritance(c, defaults) for c in config["components"]]

    registry = build_template_registry(template_dir, env)
    validate_components(components, registry, custom_template_dir)

    for comp in components:
        process_component(comp, registry, env, base_output_dir, custom_template_dir)

def load_yaml_string(data):
    try:
        return yaml.safe_load(data)
    except Exception as e:
        print(f"YAML parse error: {e}")
        return None

def build_template_registry(template_dir, env):
    registry = {}
    for filename in os.listdir(template_dir):
        match = re.match(r"(?P<type>\w+)_(?P<section>\w+)\.yaml\.j2$", filename)
        if match:
            type_ = match.group("type")
            section = match.group("section")
            registry.setdefault(type_, {})[section] = env.get_template(filename)
    return registry

def render_component(comp, registry, env, output_dir):
    comp_id = comp["id"]
    comp_type = comp["type"]
    templates = registry.get(comp_type, {})
    for section, template in templates.items():
        section_dir = os.path.join(output_dir, section)
        os.makedirs(section_dir, exist_ok=True)
        output_path = os.path.join(section_dir, f"{comp_id}.yaml")
        with open(output_path, "w") as f:
            rendered = template.render(context=comp)
            non_empty_lines = [line for line in rendered.splitlines() if line.strip()]
            f.write('\n'.join(non_empty_lines))
        print(f"[✓] {section}: {comp_id}")

def process_component(comp, registry, env, output_dir, custom_template_dir):
    comp_type = comp["type"]
    custom_template_path = os.path.join(custom_template_dir, f"{comp_type}.yaml.j2")
    if os.path.exists(custom_template_path):
        template = env.get_template(f"{comp_type}.yaml.j2")
        rendered_yaml = template.render(context=comp)
        # print the rendered YAML for debugging
        print(rendered_yaml)
        parsed = load_yaml_string(rendered_yaml)
        if parsed and "components" in parsed:
            for sub in parsed["components"]:
                process_component(sub, registry, env, output_dir, custom_template_dir)
    else:
        render_component(comp, registry, env, output_dir)

def apply_inheritance(component, defaults):
    if "extends" in component:
        base = defaults.get(component["extends"], {}).copy()
        base.update(component)
        return base
    return component

def validate_components(components, registry, custom_template_dir):
    ids = set()
    for comp in components:
        if "id" not in comp:
            raise ValueError("Component missing 'id'")
        if comp["id"] in ids:
            raise ValueError(f"Duplicate component id: {comp['id']}")
        ids.add(comp["id"])
        type_ = comp["type"]
        if type_ not in registry and not os.path.exists(os.path.join(custom_template_dir, f"{type_}.yaml.j2")):
            raise ValueError(f"Unknown component type: {type_}")

# ✅ Ensure main only runs when called directly
if __name__ == "__main__":
    main()
