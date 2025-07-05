import os
import yaml
import re
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# --- Argument parsing ---
parser = argparse.ArgumentParser(description="Generate esphome yaml from template with composable components.")
parser.add_argument("-f", "--file", required=True, help="Path to the main yaml template.")
parser.add_argument("-t", "--templates", help="Path to additional templates directory")
parser.add_argument("-o", "--output", default="output/final.yaml", help="Path to the output file (default: output/final.yaml)")

# Global registry to collect auto-collected sections
global_registry = ["interval", "globals", "script"] # Add more sections as needed

# Component registration
registered_components = []

class IndentDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)  # force indenting lists

class LiteralStr(str):
    pass

def literal_str_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

class TaggedScalar:
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value

    def __repr__(self):
        return f"{self.tag} {self.value!r}"
    
def unknown_tag_constructor(loader, tag_suffix, node):
    value = loader.construct_scalar(node)
    return TaggedScalar(f"!{tag_suffix}", value)

def tagged_scalar_representer(dumper, data):
    return dumper.represent_scalar(data.tag, data.value)

yaml.SafeLoader.add_multi_constructor('!', unknown_tag_constructor)

for dumper in (yaml.SafeDumper, IndentDumper):
    yaml.add_representer(LiteralStr, literal_str_representer, Dumper=dumper)
    yaml.add_representer(TaggedScalar, tagged_scalar_representer, Dumper=dumper)
# yaml.add_representer(TaggedScalar, tagged_scalar_representer, Dumper=yaml.SafeDumper)
# yaml.add_representer(LiteralStr, literal_str_representer, Dumper=yaml.SafeDumper)
# yaml.add_representer(LiteralStr, literal_str_representer, Dumper=IndentDumper)

def lambda_multiline_body(s):
    lines = s.strip("\n").splitlines()

    # Skip empty lines and find the first non-empty line's indentation
    for line in lines:
        if line.strip():  # line has non-space content
            match = re.match(r'^[ \t]*', line)
            base_indent = match.group(0)
            break
    else:
        return ""  # All lines are empty

    # Compile regex to strip this exact indentation
    pattern = re.compile(rf'^{re.escape(base_indent)}')
    dedented = [pattern.sub('', line) if line.startswith(base_indent) else line for line in lines]

    s = "\n".join(dedented)
    s = s.strip()

    return LiteralStr(s)

def register_component(id=None, auto_collected=None):
    if auto_collected is None:
        auto_collected = {}
    registered_components.append({
        "id": id,
        "auto_collected": auto_collected
    })
    print(f"[✓] Registered component: {id}")

def collect_section(section):
    merged = []
    for comp in registered_components:
        part = comp["auto_collected"].get(section)
        if part:
            merged.extend(part)
    return merged

def render_main_template(env, template_name, context):
    template = env.get_template(template_name)
    return template.render(**context)

def register_all_macros(env, templates_dir):
    """
    Automatically registers all macros from .j2 files in the templates directory as globals.
    """
    print(f"Registering macros from templates in {templates_dir}")
    for template_path in Path(templates_dir).glob("*.j2"):
        template = env.get_template(template_path.name)
        # Iterate over all attributes in the template module
        for attr_name in dir(template.module):
            attr = getattr(template.module, attr_name)
            # Only add callable macros (skip private and built-ins)
            if callable(attr) and not attr_name.startswith("_"):
                env.globals[attr_name] = attr
                print(f"[✓] Registering macro: {attr_name}")



def main():
    args = parser.parse_args()

    templates_dir = None
    if args.templates:
        templates_dir = Path(args.templates).resolve()
    # Calculate the current file path
    current_file_directory = Path(__file__).parent
    output_file = args.output
    main_template_file = args.file
    main_template_file_parent = Path(main_template_file).parent
    output_dir = Path(output_file).parent

    templates_sources = [current_file_directory / "templates"]
    if templates_dir:
        templates_sources.append(templates_dir)
    
    print(f"Registring templates recursively from: {templates_sources}")

    all_template_dirs = set()
    all_template_dirs.add(main_template_file_parent)
    for template_dir in templates_sources:
        # Recursively collect all directories under templates_dir, including itself
        for root, _, _ in os.walk(template_dir):
            all_template_dirs.add(Path(root))

    env = Environment(
        loader=FileSystemLoader(all_template_dirs),
        extensions=["jinja2.ext.do"],
        trim_blocks=True,
        lstrip_blocks=True
    )
    env.globals.update({
        "register_component": register_component,
        "lambda_multiline_body": lambda_multiline_body
    })

    # Go over all dirs in template_dirs and register macros
    for template_dir in all_template_dirs:
        if template_dir is not main_template_file_parent:
            register_all_macros(env, template_dir)

    print("\n")
    print(f"Rendering main template {main_template_file}...")
    rendered = render_main_template(env, Path(main_template_file).name, {})

    # Load the user-rendered content
    parsed_yaml = yaml.safe_load(rendered)

    # Merge auto-collected sections into the root-level YAML
    for section in global_registry:
        parsed_yaml.setdefault(section, [])
        parsed_yaml[section].extend(collect_section(section))

    print("\n")
    print(f"Writing output to {output_file}...")
    
    output_dir.mkdir(exist_ok=True)
    # Write final output
    with open(output_file, "w") as f:
        yaml.dump(parsed_yaml, f, Dumper=IndentDumper, indent=2, default_flow_style=False, sort_keys=False)

    print("Done!")

if __name__ == "__main__":
    main()