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


def fill_in_template(template, vars):
    """
    >>> template = '{plants} are {color}'
    >>> vars = {'plants': 'roses', 'color': 'red', 'extra': 'Dont care'}
    >>> fill_in_template(template, vars)
    'roses are red'
    >>> fill_in_template(template, {'plants': 'trees'})
    Traceback (most recent call last):
       ...
    KeyError: "Missing key 'color' for template '{plants} are {color}'"
    """
    template_vars = [f[1] for f in string.Formatter().parse(template) if f[1]]
    for var in template_vars:
        if var not in vars:
            raise KeyError(f"Missing key '{var}' for template '{template}'")
    return template.format(**vars)


def get_url_and_payload(prompt_settings):
    """
    >>> settings = {'providers':
    ...                 {'foo':
    ...                      {'bar-service':
    ...                          {'url': 'https://example.com/{engine}',
    ...                           'args': ['temperature']}}},
    ...             'provider': 'foo', 'service': 'bar-service', 'engine': 'steam', 'temperature': 1, 'extra': 42}
    >>> get_url_and_payload(settings)
    ('https://example.com/steam', {'temperature': 1})
    """
    provider = prompt_settings['provider']
    service = prompt_settings['service']
    service_settings = prompt_settings['providers'][provider][service]
    url_template = service_settings['url']
    url = fill_in_template(url_template, prompt_settings)
    accepted_keys = service_settings['args']
    payload = {k: prompt_settings[k] for k in prompt_settings.keys() if k in accepted_keys}
    return url, payload


def generate(prompt_file):
    prompts = load_yaml(prompt_file)
    prompt_settings = merge_by_keys(prompts)
    url, payload = get_url_and_payload(prompt_settings)



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_file")
    args = parser.parse_args()
    if not set_api_key():
        return
    generate(args.prompt_file)


if __name__ == "__main__":
    parse_arg()
