import argparse
import copy
import os
import openai
import ruamel.yaml as yaml

DEFAULT_ENGINE_EDIT = 'text-davinci-edit-001'
DEFAULT_ENGINE_COMPLETION = 'text-davinci-002'

yaml.allow_unicode = True
yaml.width = 80


def set_api_key():
    try:
        import secretenvvars
        openai.api_key = secretenvvars.openai_api_key
    except ImportError:
        openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        print("API key not found")
        return False
    return True


def load_yaml(fname):
    pass

def merge_by_keys(dicts):
    """
    >>> dicts = [{'foo': 'old', 'unique': 1}, {'foo': 'new', 'new_key': 2}]
    >>> merge_by_keys(dicts)
    {'foo': 'new', 'unique': 1, 'new_key': 2}
    """
    merged = {}
    for d in dicts:
        merged |= d
    return merged

def generate(prompt_file):
    prompts = yaml_file_to_dicts(prompt_file)
    params = merge_by_keys(prompts)



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_file")
    args = parser.parse_args()
    if not set_api_key():
        return
    generate(args.prompt_file)


if __name__ == "__main__":
    parse_arg()
