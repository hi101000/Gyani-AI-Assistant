import json
import os
import helpers
from datetime import datetime, date
import requests
from bs4 import BeautifulSoup
import sys
from random import choice
from serpapi import GoogleSearch

def search_google(keyword):
    key = ""
    with open("Gyani/serp_key.txt", "r") as f:
        key = f.read()
    search = GoogleSearch({
      "q": keyword,
      "location": "Austin,Texas",
      "api_key": key
    })
    print(search.get_dict()["knowledge_graph"]["description"])
    # with open("Gyani/google_json.json", "w") as f:
    #   json.dump(search.get_dict(), f)
    return search.get_dict()["knowledge_graph"]["description"]

def open_app(app_name: str) -> None:
  app_name = f'{app_name}.app'
  """
  Attempts to launch the application with the given name.
  Args:
      app_name: The name of the application to open (e.g., "Github Desktop" or its full path).

  Returns:
      None
  """

# Example usage
  apps = helpers.find_file_in_directories(app_name)

  if len(apps)>=1:
    # Handle multiple matches (prompt user, provide more info)
    
    for app in apps:
      os.system(f'open {"\ ".join(app.split(" "))}')
  else:
    return f"No application found matching '{app_name}'."
  return f"Found applications matching '{app_name}':"

def send_message(who: str, message:str) -> str:
  os.system(f'osascript message.applescript {who} "{message}"')
  return f"sent message \"{message}\" to recipient {who}"

def get_time() -> str:
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  return current_time

def get_date() -> str:
  return date.today()

def get_weather(place: str) -> str:
  url = f'https://www.google.com/search?q=+"weather"+{place}'
  html = requests.get(url).content
  soup = BeautifulSoup(html, 'html.parser')
  # get the temperature
  temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text

  # this contains time and sky description
  str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

  # format the data
  data = str.split('\n')
  time = data[0]
  sky = data[1]
  # list having all div tags having particular class name
  listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})

  # particular list with required data
  strd = listdiv[5].text

  # formatting the string
  pos = strd.find('Wind')
  other_data = strd[pos:]
  # printing all the data
  return f"The temperature in {place} is {temp}, the time is {time}, the sky is {sky}, and here's some other relevant information:\n{other_data}"

def leave() -> None:
  sys.exit(0)

def open_site(site_name: str) -> str:
  import webbrowser
  webbrowser.open(site_name)
  return f"I have opened {site_name}"

def write_to_file(fname: str, content: str) -> str:
  with open(fname, "w") as f:
    f.write(content)
  return f"wrote {content} to {fname}"

def open_file(fname: str) -> str:
  fname = '\ '.join(fname.split(" "))
  os.system(f"open {fname}")
  return f"opened {fname}"

def get_headlines_for_a_topic(topic: str) -> str:
    url = f'https://www.bbc.com/search?q={"+".join(topic.split(" "))}'
    response = requests.get(url) 

    soup = BeautifulSoup(response.text, 'html.parser') 
    headlines = soup.find('body').find_all('h2')
    temp = [] 
    if len(headlines) <= 20:
      length = len(headlines)
    else:
      length = 20
    for x in range(0, length): 
        temp.append(headlines[x].text.strip())
    headlines = '\n'+'\n'.join(temp)
    del temp
    return headlines

def get_generic_headlines() -> str:
  url = 'https://www.bbc.com/news'
  response = requests.get(url)
    
  soup = BeautifulSoup(response.text, 'html.parser') 
  headlines = soup.find('body').find_all('h2') 
  unwanted = ['BBC World News TV', 'BBC World Service Radio', 
              'News daily newsletter', 'Mobile app', 'Get in touch', "Trending Topics"] 
  headlines = list(dict.fromkeys(headlines))
  if len(headlines) <= 20:
    length = len(headlines)
  else:
    length = 20
  temp = []
  for x in range(0, length): 
      if headlines[x].text.strip() not in unwanted: 
          temp.append(headlines[x].text.strip())

  url = "https://ground.news/blindspot"
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser') 
  headlines = soup.find('body').find_all('h4')
  headlines = list(dict.fromkeys(headlines))
  for x in range(0, len(headlines)): 
      if headlines[x].text.strip() not in unwanted: 
          temp.append(headlines[x].text.strip())



  headlines = temp
  del temp
  headlines = '\n' + '\n\n'.join(headlines)
  return headlines



functions = [
  {
      "name": "open_app",
      "description": "used to open an app, if that is what the user asks for",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": {
            "type": "string",
            "description": "the name of the app as provided by the user (e.g. if the user says 'open Github Desktop', then this argument would be 'Github Desktop')"
          }
        }
      }
    },
  {
    "name":"send_message",
    "description":"used to send messages through iMessage, if the user requests it",
    "parameters":{
       "type":"object",
       "properties":{
         "who":{
           "type":"string",
           "description":"the recipient of the message"
         },
         "message":{
           "type":"string",
           "description":"the message contents"
         }
       }
    }
    },
  {
      "name":"get_time",
      "description":"used to get the current time, if the user asks for it",
      "parameters":{}
  },
  {
    "name":"get_date",
    "description":"used to get the date, if the user requests it",
    "parameters":{}
  },
  {
    "name":"get_weather",
    "description":"used to get details about the weather in a place that the user specifies",
    "parameters":{
      "type":"object",
      "properties":{
        "place":{
          "type":"string",
          "description":"the place for which the user has requested weather details."
        }
      }
    }
  },
  {
    "name":"leave",
    "description":"used to exit the program if the user desires this",
    "parameters":{}
  },
  {
    "name":"open_site",
    "description":"opens a website, if the user requests it",
    "parameters":{
      "type":"object",
      "properties":{
        "site_name":{
          "type":"string",
          "description":"the url of the website that you have constructed based on the user's request"
        }
      }
    }
  },
  {
    "name":"write_to_file",
    "description":"writes user-specified content to a user-specified file",
    "parameters":{
      "type":"object",
      "properties":{
        "fname":{
          "type":"string",
          "description":"the user-specified file name"
        },
        "content":{
          "type":"string",
          "description":"the user-specified content to write to the files"
        }
      }
    }
  },
  {
    "name":"open_file",
    "description":"opens a user-specified file",
    "parameters":{
      "type":"object",
      "properties":{
        "fname":{
          "type":"string",
          "description":"the user-specified file name"
        }
      }
    }
  },
  {
    "name":"get_headlines_for_a_topic",
    "description":"retreives headlines for a user-specified topic when the user asks for news specifically pertaining to one topic",
    "parameters":{
      "type":"object",
      "properties":{
        "topic":{
          "type":"string",
          "description":"the user-specified topic to search for"
        }
      }
    }
  },
  {
    "name":"get_generic_headlines",
    "description":"retreives various generic headlines; for use when user wants news but does not specify a topic",
    "parameters":{}
  },
{
    "name":"search_google",
    "description":"searches google for specified keyword(s)",
    "parameters":{
      "type":"object",
      "properties":{
        "keyword":{
          "type":"string",
          "description":"the user-specified keyword(s) to search for"
        }
      }
    }
  }
]
