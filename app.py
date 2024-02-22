import os
import streamlit as st
from langchain_community.llms import openai
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file


# App framework
st.title('🦜🔗 Youtube GPT Creator')
prompt = st.text_input('Plug in your prompt here')

# 
template_string = '''Write a Youtube video title about {topic}.
'''
title_template = PromptTemplate.from_template(template_string)
# title_template = ChatPromptTemplate.from_template(template_string)

# LLM
# llm = OpenAI(temperature=0.9)
llm = ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo-0125")
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True)


# Output rendering
if prompt:
    response = title_chain.run(prompt)
    st.write(response)