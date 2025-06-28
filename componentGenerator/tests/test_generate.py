import pytest
import yaml
from componentGenerator.generate import to_nice_yaml, load_yaml_string, build_template_registry, process_component
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

def test_yaml_validity():
  yaml_str = """
  components:
    - id: test_timer
      type: arc_countdown
      duration: 3000
      on_countdown_done:
        - logger.log: "Done!"
  """
  data = load_yaml_string(yaml_str)
  assert data["components"][0]["id"] == "test_timer"

def test_custom_component_expansion(tmp_path):
  template_dir = "componentGenerator/templates"
  custom_template_dir = "componentGenerator/custom_templates"
  output_dir = "components"

  env = Environment(loader=FileSystemLoader([template_dir, custom_template_dir]))
  env.filters['to_nice_yaml'] = to_nice_yaml

  registry = build_template_registry(template_dir, env)
  comp = {
      "id": "test_timer",
      "type": "arc_countdown",
      "duration": 3000,
      "on_countdown_done_callback": "done_callback_script"
  }
  process_component(comp, registry, env, output_dir, custom_template_dir)
  assert (Path("components/test_timer_arc/widget.yaml").exists())
