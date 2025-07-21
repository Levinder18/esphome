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

class MacroNamespace:
    pass

# Component registration
registered_components = []

class IndentDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)  # force indenting lists

# Custom representer for str to handle values starting with '!'
def custom_str_representer(dumper, data):
    if isinstance(data, str) and data.startswith("!"):
        # Split the tag and value
        if " " in data:
            tag, value = data.split(" ", 1)
        elif "\n" in data:
            tag, value = data.split("\n", 1)
        else:
            tag, value = data, ""
        return dumper.represent_scalar(tag, value.lstrip())
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

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
# yaml.SafeLoader.add_multi_constructor('|', literal_str_representer)


for dumper in (yaml.SafeDumper, IndentDumper):
    yaml.add_representer(LiteralStr, literal_str_representer, Dumper=dumper)
    yaml.add_representer(TaggedScalar, tagged_scalar_representer, Dumper=dumper)
    yaml.add_representer(str, custom_str_representer, Dumper=dumper)

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

def collect_all_macros(env, template_dirs):
    """
    Collect all macros from all .j2 files in all template_dirs.
    Returns a dict: {macro_name: macro_callable}
    """
    all_macros = {}
    for template_dir in template_dirs:
        print(f"Registering macros from templates in {template_dir}")
        for template_path in Path(template_dir).glob("*.j2"):
            template = env.get_template(template_path.name)
            for attr_name in dir(template.module):
                attr = getattr(template.module, attr_name)
                if callable(attr) and not attr_name.startswith("_"):
                    all_macros[attr_name] = attr
                    print(f"[✓] Found macro: {attr_name}")
    return all_macros

def wrap_macro(macro_func, all_macros):
    def wrapped_macro(*args, **kwargs):
        for name, func in all_macros.items():
            if name not in kwargs:
                kwargs[name] = func
        return macro_func(*args, **kwargs)
    return wrapped_macro

def generate_dispatch_lambda(script_names):
    lines = []
    lines.append('if (false) {}')  # trick to simplify `else if` chains

    for script in script_names:
        # Prepare param list string for call
        lines.append(f'else if (name == "{script}") {{')
        lines.append(f'  id({script}).execute();')
        lines.append('  return;')
        lines.append('}')
    lines.append('ESP_LOGW("dispatcher", "Unknown script name: %s", name.c_str());')
    return '\n'.join(lines)

def generate_script_dispatcher(scripts):
    supported_script_names = [script['id'] for script in scripts if 'parameters' not in script]

    return {
        'id': 'script_dispatcher',
        'parameters': {'name': 'std::string'},
        'then': [
            {
                'lambda': lambda_multiline_body(generate_dispatch_lambda(supported_script_names))
            }
        ]
    }

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

    # --- NEW: Collect and wrap all macros ---
    all_macros = collect_all_macros(env, [dir for dir in all_template_dirs if dir is not main_template_file_parent])
    # wrapped_macros = {name: wrap_macro(func, all_macros) for name, func in all_macros.items()}
    # env.globals.update(wrapped_macros)
    env.globals.update(all_macros.items())

    macro_ns = MacroNamespace()
    for name, func in all_macros.items():
        setattr(macro_ns, name, func)

    env.globals['macros'] = macro_ns

    print("\n")
    print(f"Rendering main template {main_template_file}...")
    rendered = render_main_template(env, Path(main_template_file).name, {})

    # Load the user-rendered content
    try:
        parsed_yaml = yaml.safe_load(rendered)
    except yaml.YAMLError as e:
        print(f"Complete YAML content:\n{rendered}")
        print(f"Error parsing YAML: {e}")
        return

    # Dynamically determine all unique section names from auto_collected of registered_components
    all_sections = set()
    for comp in registered_components:
        all_sections.update(comp["auto_collected"].keys())

    # Merge auto-collected sections into the root-level YAML
    for section in all_sections:
        parsed_yaml.setdefault(section, [])
        parsed_yaml[section].extend(collect_section(section))

    # Add the dispatcher
    if 'script' not in parsed_yaml:
        parsed_yaml['script'] = []
    parsed_yaml['script'].append(generate_script_dispatcher(parsed_yaml['script']))

    print("\n")
    print(f"Writing output to {output_file}...")
    
    output_dir.mkdir(exist_ok=True)
    # Write final output
    with open(output_file, "w") as f:
        yaml.dump(parsed_yaml, f, Dumper=IndentDumper, indent=2, default_flow_style=False, sort_keys=False)

    print("Done!")

if __name__ == "__main__":
    main()