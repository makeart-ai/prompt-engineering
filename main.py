import argparse
import os
import openai
import requests
import ruamel.yaml as yaml
import string


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
    with open(fname) as file:
        return yaml.safe_load(file)


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


def json_from_url(url, token, payload=None):
    headers = {"Authorization": "Bearer {}".format(token)}
    return requests.get(url, headers=headers, data=payload).json()


def get_service_url(prompt_settings):
    """
    >>> settings = {'providers':
    ...                 {'foo':
    ...                      {'bar-service':
    ...                          {'url': 'https://example.com/{engine}',
    ...                           'args': ['temperature']}}},
    ...             'provider': 'foo', 'service': 'bar-service', 'engine': 'steam', 'temperature': 1, 'other': 42}
    >>> get_service_url(settings)
    'https://example.com/steam'
    """
    provider = prompt_settings['provider']
    service = prompt_settings['service']
    service_settings = prompt_settings['providers'][provider][service]
    url_template = service_settings['url']
    template_var_names = [f[1] for f in string.Formatter().parse(url_template) if f[1]]
    template_vars = {k: prompt_settings[k] for k in prompt_settings.keys() if k in template_var_names}
    url = url_template.format(**template_vars)
    return url


def generate(prompt_file):
    prompts = load_yaml(prompt_file)
    prompt_settings = merge_by_keys(prompts)
    url = get_service_url(prompt_settings)



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_file")
    args = parser.parse_args()
    if not set_api_key():
        return
    generate(args.prompt_file)


if __name__ == "__main__":
    parse_arg()
