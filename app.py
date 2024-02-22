import os
import streamlit as st
from langchain_community.llms import openai
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain, SequentialChain


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file


# App framework
st.title('🦜🔗 Youtube GPT Creator')
prompt = st.text_input('Plug in your topic here')

# Prompt templates
# title_template = ChatPromptTemplate.from_template(template_string)
title_prompt = PromptTemplate.from_template('Write a Youtube video title about {topic}.')
script_prompt = PromptTemplate.from_template('Write a Youtube video script based on this title.\nTITLE: {title}')

# LLM
# llm = OpenAI(temperature=0.9)
llm = ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo-0125")
title_chain = LLMChain(llm=llm, prompt=title_prompt, output_key='title', verbose=True)
script_chain = LLMChain(llm=llm, prompt=script_prompt, output_key='script', verbose=True)

sequential_chain = SequentialChain(
    chains=[title_chain, script_chain], 
    input_variables= ['topic'], 
    output_variables= ['title', 'script'],
    verbose=True
)


# Output rendering
if prompt:
    response = sequential_chain({'topic': prompt})
    st.write(response['title'])
    st.write(response['script'])