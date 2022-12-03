import argparse
from dotenv import load_dotenv
import json
import os
import openai
import requests
import ruamel.yaml as yaml
import string


yaml.allow_unicode = True
yaml.width = 80


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


def json_from_url(url, method, token, payload=None):
    """@return is_success, json_response"""
    headers = {"Authorization": f"Bearer {token}"}
    print(f"request: {method} {url} {payload}")
    response = requests.request(method, url, headers=headers, json=payload)
    return response.status_code == 200, response.json()


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
    method = service_settings['method']
    payload = {k: prompt_settings[k] for k in prompt_settings.keys() if k in accepted_keys}
    return url, method, payload


def get_token(settings):
    provider = settings["provider"]
    key = f"{provider}_token"
    load_dotenv()
    return os.environ.get(key)


def append_as_yaml(fname, obj):
    as_yaml = "\n" + yaml.safe_dump([obj])
    print(f'as_yaml {as_yaml}')
    with open(fname, 'a') as file:
        file.write(as_yaml)


def generate(prompt_file):
    prompts = load_yaml(prompt_file)
    prompt_settings = merge_by_keys(prompts)
    url, method, payload = get_url_and_payload(prompt_settings)
    token = get_token(prompt_settings)
    is_success, response = json_from_url(url, method, token, payload)
    if is_success:
        append_as_yaml(prompt_file, response)
    else:
        print(f"Error {response}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_file")
    args = parser.parse_args()
    generate(args.prompt_file)


if __name__ == "__main__":
    main()
