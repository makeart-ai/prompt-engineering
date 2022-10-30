import os
import openai

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

def main():
    if not setApiKey():
        return
    completion = openai.Completion.create(engine="ada", prompt="Hello")
    print(completion.choices[0].text)


if __name__ == "__main__":
    main()