import yaml

class LiteralStr(str):
    pass

def literal_str_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

yaml.add_representer(LiteralStr, literal_str_representer, Dumper=yaml.SafeDumper)

data = {
    "then": [
        {"lambda": LiteralStr("id(my_lambda).execute();ESP_LOGI(\"x\", \"ok\");")}
    ]
}

print(yaml.dump(data, Dumper=yaml.SafeDumper, sort_keys=False))