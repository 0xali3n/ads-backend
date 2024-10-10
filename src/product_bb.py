import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def product_recog(imageUrl,user_gen_id):
  azure_computer_vision_endpoint = "https://edictai-background-remover-2.cognitiveservices.azure.com/computervision" # put in environment variable
  modelName = "ms-pretrained-product-detection" # put in environment variable
  taskName = f"recog_{user_gen_id}" # put unique task name for each request

  url = f"{azure_computer_vision_endpoint}/productrecognition/{modelName}/runs/{taskName}?api-version=2023-04-01-preview"

#   imageUrl = "https://i.ibb.co/YpypHxR/ponds.jpg" # put image link here

  payload = json.dumps({
    "url": imageUrl
  })

  computervision_api_key = os.environ.get("COMPUTERVISION_API_KEY") # put in environment variable

  headers = {
    'Ocp-Apim-Subscription-Key': computervision_api_key,
    'Content-Type': 'application/json'
  }

  response = requests.request("PUT", url, headers=headers, data=payload)

  print(response.text)
  result = response.text
  return result



def get_bb(recognized_pdt,user_gen_id):
    azure_computer_vision_endpoint = "https://edictai-background-remover-2.cognitiveservices.azure.com/computervision" # put in environment variable
    modelName = "ms-pretrained-product-detection" # put in environment variable
    taskName =  f"recog_{user_gen_id}" # put unique task name for each request

    url = f"{azure_computer_vision_endpoint}/productrecognition/{modelName}/runs/{taskName}?api-version=2023-04-01-preview"

    computervision_api_key = os.environ.get("COMPUTERVISION_API_KEY") # put in environment variable

    payload = {}
    headers = {
    'Ocp-Apim-Subscription-Key': computervision_api_key
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    result = response.text
    return result