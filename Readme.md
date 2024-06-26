# Gyani AI Assistant

## About
Gyani (well, the proper transliteration would be Gyaani) is a [Hindi adjective meaning "wise" or "knowledgable."](https://en.wiktionary.org/wiki/ज्ञानी#Hindi) That is what Gyani is supposed to be: a knowledgable and helpful AI assistant who can talk with you like ChatGPT but can help you with your device like Siri does.

## API Key
You will need to add a key.txt file with your openai api key in the Gyani directory. Alternatively, you could change the code near the start of ai.py from

```
with open("key.txt", "r") as f:
    openai.api_key = f.read()
```

to 

```
openai.api_key = "API_KEY"
```

## Compilation

To compile this, you will need to install nuitka, which is included in requirements.txt.
If you do not want to compile this to a standalone binary and just want to run the python code, feel free to remove nuitka from requirements.txt before installing it using ```pip install -r requirements.txt``` and also feel free to delete ```compile.sh```