import os
import streamlit as st
# from langchain_community.llms import openai
from langchain_openai import OpenAI, ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities.wikipedia import WikipediaAPIWrapper
# from langchain_community.utilities import wikipedia


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file


# App framework
st.title('🦜🔗 Youtube Video Script Creator')
prompt = st.text_input('Plug in your topic here')

# Prompt templates
title_prompt = ChatPromptTemplate.from_template('Write a Youtube video title about {topic}.')
script_prompt = ChatPromptTemplate.from_template('Write a Youtube video script based on this title: {title} \
    while leveraging this Wikipedia research: {wikipedia_research}')
# title_prompt = PromptTemplate(
#     input_variables = ['topic'], 
#     template='write me a youtube video title about {topic}'
# )

# script_prompt = PromptTemplate(
#     input_variables = ['title', 'wikipedia_research'], 
#     template='write me a youtube video script based on this title TITLE: {title} while leveraging this wikipedia reserch:{wikipedia_research} '
# )


# Memory
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')

# LLM
# llm = OpenAI(temperature=0.9)
llm = ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo-0125")
title_chain = LLMChain(llm=llm, prompt=title_prompt, output_key='title', verbose=True, memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_prompt, output_key='script', verbose=True, memory=script_memory)

# sequential_chain = SequentialChain(
#     chains=[title_chain, script_chain], 
#     input_variables= ['topic'], 
#     output_variables= ['title', 'script'],
#     verbose=True
# )

# Output rendering
if prompt:
    # response = sequential_chain({'topic': prompt})
    title = title_chain.run(prompt)
    wikipedia_research = WikipediaAPIWrapper().run(prompt)
    script = script_chain.run(title=title, wikipedia_research=wikipedia_research)
    
    st.write(title)
    st.write(script)
    
    
    with st.expander('Title History'):
        st.info(title_memory.buffer)
        
    with st.expander('Script History'):
        st.info(script_memory.buffer)
        
    with st.expander('Wikipedia Research'):
        st.info(wikipedia_research)