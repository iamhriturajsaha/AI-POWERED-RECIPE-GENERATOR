## **Installation**
"""

!pip install datasets huggingface_hub -q
!pip install -q -U transformers
!pip install -q bitsandbytes==0.41.3 accelerate==0.25.0
!pip install langchain -q
!pip install openai langchain_openai -q
!pip install typing_extensions

!pip install pyttsx3 # library for coverting text to speech

!pip install gtts

from google.colab import userdata
OPENAI_API_KEY=userdata.get('OPENAI_API_KEY')

"""## **Login to Huggingface**"""

from huggingface_hub import login
login()

"""## **Get the image of the food you want to cook**"""

import requests
from PIL import Image
image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3ZKlfd82ogR-0YWf882ZQMQDp9dxDb9KszkCpA2WRFw&s"
image = Image.open(requests.get(image_url, stream=True).raw)
image

"""## **Using The AI Model**"""

from transformers import pipeline
captioner= pipeline("image-to-text", model ="Salesforce/blip-image-captioning-base")

results = captioner(image_url)
print(results[0]['generated_text'])

"""## **Using Langchain to access OpenAI**"""

from langchain_openai import OpenAI

llm = OpenAI(temperature=0,max_tokens=512, openai_api_key=OPENAI_API_KEY)

llm=OpenAI(model_name="gpt-3.5-turbo-1106",temperature=0,max_tokens=512, openai_api_key='OPENAI_API_KEY')

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

template= """Question: {question}
Answer: Lets think step by step,"""

prompt = PromptTemplate(template=template, input_variables=["question"])

llm_chain = LLMChain(prompt=prompt, llm=llm)

question= f"give me the list of ingredients and a step by step recipie for {results[0]['generated_text']}"

openai_results = llm_chain.invoke(question)

print(openai_results['text'])

recipe_text=openai_results['text']

from gtts import gTTS
import os

def text_to_speech(text, filename='recipe_audio.mp3'):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    print(f"Audio saved as {filename}")

text_to_speech(recipe_text)
