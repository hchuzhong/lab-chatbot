import requests
import os

class HKBU_ChatGPT():
  def __init__(self):
    self.config = {
      'CHATGPT_BASICURL': os.getenv('CHATGPT_BASICURL'),
      'CHATGPT_MODELNAME': os.getenv('CHATGPT_MODELNAME'),
      'CHATGPT_APIVERSION': os.getenv('CHATGPT_APIVERSION'),
      'CHATGPT_ACCESS_TOKEN': os.getenv('CHATGPT_ACCESS_TOKEN')
    }

  def submit(self, message):
    conversation = [{"role": "user", "content": message}]

    url = (self.config['CHATGPT_BASICURL']) + "/deployments/" + (self.config['CHATGPT_MODELNAME']) + "/chat/completions/?api-version=" + (self.config['CHATGPT_APIVERSION'])

    headers = {
        'api-key': (self.config['CHATGPT_ACCESS_TOKEN']),
        'Content-Type': 'application/json'
    }
    payload = { "messages": conversation }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
      data = response.json()
      return data['choices'][0]['message']['content']
    else:
      return "Error: " + response.text
    
if __name__ == "__main__":
  chatgpt = HKBU_ChatGPT()
  
  while True:
    user_input = input("Typing anything to ChatGPT:\t")
    response = chatgpt.submit(user_input)
    print(response)
