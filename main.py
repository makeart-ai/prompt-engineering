import argparse
import copy
import os
import openai
import yaml

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

class Prompt:

    def __init__(self, input, engine='davinci'):
        self.input = input
        self.engine = engine

    def execute(self):
        if self.output:
            newPrompt = Prompt(self.input, self.engine)
        else:
            newPrompt = self
        completion = openai.Completion.create(engine=self.engine, prompt=self.input)
        newPrompt.output = completion.choices[0].text
        return newPrompt


def generate(promptFile):
    if not setApiKey():
        return
    with open(promptFile) as promptsRead:
        rawPrompts = yaml.safe_load(promptsRead)
        newPrompt = rawPrompts[-1]
        if 'output' in newPrompt:
            newPrompt = copy.deepcopy(newPrompt)
            rawPrompts.append(newPrompt)
        completion = openai.Completion.create(engine="ada", prompt=newPrompt["input"])
        newPrompt['output'] = completion.choices[0].text
        print(completion.choices[0].text)
    with open(promptFile, 'w') as promptsToWrite:
        yaml.dump(rawPrompts, promptsToWrite)

def parseArgs():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")
    parserNew = subparsers.add_parser("new", help="Create new prompt file")
    parserGen = subparsers.add_parser("gen", help="Generate new output from prompt")
    parserGen.add_argument("promptFile")

    args = parser.parse_args()
    if args.subcommand == "gen":
        generate(args.promptFile)
    else:
        print("TODO: finish arg parsing")


if __name__ == "__main__":
    parseArgs()