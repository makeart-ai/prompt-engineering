import argparse
import copy
import os
import openai
import ruamel.yaml as yaml
import time

DEFAULT_ENGINE_EDIT = 'text-davinci-edit-001'
DEFAULT_ENGINE_COMPLETION = 'text-davinci-002'

yaml.allow_unicode = True
yaml.width = 80

def setApiKey():
    try:
        import secretenvvars
        openai.api_key = secretenvvars.openai_api_key
    except ImportError:
        openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        print("API key not found")
        return False
    return True

def generate(promptFile):
    with open(promptFile) as promptsRead:
        rawPrompts = yaml.safe_load(promptsRead)
        newPrompt = rawPrompts[-1]
        if 'output' in newPrompt:
            newPrompt = copy.deepcopy(newPrompt)
            rawPrompts.append(newPrompt)
        if 'instruction' in newPrompt:
            engine = newPrompt.get('engine', DEFAULT_ENGINE_EDIT)
            response = openai.Edit.create(engine=engine, input=newPrompt["input"], instruction=newPrompt["instruction"], temperature=0.94)
            newPrompt['output'] = response.choices[0].text.strip()
        else:
            engine = newPrompt.get('engine', DEFAULT_ENGINE_COMPLETION)
            input = newPrompt['input']
            temperature = 1
            for top_p in [0.1 + i/10 for i in range(10)]:
                for _ in range(3):
                    output = get_completion(input, temperature, top_p)
                    one_new = dict(top_p=top_p, temperature=temperature, output=output)
                    rawPrompts.append(one_new)
            top_p = 1
            for temperature in [i/10 for i in range(11)]:
                for _ in range(3):
                    output = get_completion(input, temperature, top_p)
                    one_new = dict(top_p=top_p, temperature=temperature, output=output)
                    rawPrompts.append(one_new)
    with open(promptFile, 'w') as promptsToWrite:
        yaml.dump(rawPrompts, promptsToWrite, default_style="|")


def get_completion(input, temperature, top_p):
    time.sleep(2)
    response = openai.Completion.create(engine=DEFAULT_ENGINE_COMPLETION, prompt=input, temperature=temperature, max_tokens=256, frequency_penalty=1, top_p=top_p)
    return response.choices[0].text.strip()

def listEngines():
    engines = openai.Engine.list()
    engineNames = [engine.id for engine in engines.data]
    print(engineNames)

def parseArgs():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")
    parserNew = subparsers.add_parser("new", help="Create new prompt file")
    parserGen = subparsers.add_parser("gen", help="Generate new output from prompt")
    parserListEngines = subparsers.add_parser("listEngines")
    parserGen.add_argument("promptFile")

    args = parser.parse_args()
    if not setApiKey():
        return
    if args.subcommand == "gen":
        generate(args.promptFile)
    elif args.subcommand == "listEngines":
        listEngines()
    else:
        print("TODO: finish arg parsing")


if __name__ == "__main__":
    parseArgs()