import openai
import functions
import json

conversation = [
    {"role": "system", "content": """You are an AI assistant named Gyani who can control the user's device to function in a manner not dissimilar to that of Siri. You have been provided with the list of functions available to you, and shall use these functions to serve the user."""},
]

with open("key.txt", "r") as f:
    openai.api_key = f.read()

def ask_system(message: str):
    conversation.append({"role": "system", "content": message})  
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=conversation,
        max_tokens=200,)

    return response.choices[0].message.content

def ask(message: str):
        conversation.append({"role": "user", "content": message})  
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=conversation,
            max_tokens=200,
            functions = functions.functions, 
            function_call = "auto")

        if response['choices'][0]['finish_reason'] == "function_call":
            args = []
            argus = json.loads(f"[{response['choices'][0]['message']['function_call']['arguments']}]")
            for arg in argus:
                for index in arg.keys():
                    args.append(f'\"{arg[index]}\"')
            re = f"{response['choices'][0]['message']['function_call']['name']}({','.join(args)})"
            conversation.append({"role": "assistant", "content": re})
            return eval(f'functions.{re}')
            
            
        else:
            conversation.append({"role": "assistant", "content": response.choices[0].message.content})
        response = response.choices[0].message.content
        return response
