import streamlit as st
import time
import psutil
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACKING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries"),
        ("user", "Question:{question}")
    ]
)

# OpenAI LLM
llm_openai = ChatOpenAI(model="gpt-3.5-turbo")
output_parser_openai = StrOutputParser()
chain_openai = prompt | llm_openai | output_parser_openai

# Local LLM (Ollama Mistral)
llm_local = Ollama(model="Mistral")
output_parser_local = StrOutputParser()
chain_local = prompt | llm_local | output_parser_local

st.title('Model Performance Comparison')

input_text = st.text_input("Write your query over here.")

# Function to measure response time
def measure_response_time(chain, query):
    start_time = time.time()
    response = chain.invoke({'question': query})
    end_time = time.time()
    return response, end_time - start_time

# Function to measure CPU and memory usage
def measure_resource_usage():
    cpu_usage = psutil.cpu_percent(interval=1)  # Measures CPU usage over a 1-second interval
    memory_info = psutil.virtual_memory()       # Gets virtual memory usage statistics
    return cpu_usage, memory_info.percent       # Returns CPU usage and percentage of memory usage

if input_text:
    # Measure response time for OpenAI GPT-3.5-turbo
    response_openai, time_openai = measure_response_time(chain_openai, input_text)
    # Measure response time for Local LLM (Ollama Mistral)
    response_local, time_local = measure_response_time(chain_local, input_text)
    
    # Display responses
    st.write("OpenAI GPT-3.5-turbo Response:", response_openai)
    st.write("Local LLM (Ollama Mistral) Response:", response_local)
    
    # Measure resource usage for OpenAI GPT-3.5-turbo
    cpu_openai, memory_openai = measure_resource_usage()
    # Measure resource usage for Local LLM (Ollama Mistral)
    cpu_local, memory_local = measure_resource_usage()
    
    # Create a comparison table
    comparison_data = {
        'Metric': ['Response Time (s)', 'CPU Usage (%)', 'Memory Usage (%)'],
        'OpenAI GPT-3.5-turbo': [time_openai, cpu_openai, memory_openai],
        'Local LLM (Ollama Mistral)': [time_local, cpu_local, memory_local]
    }
    
    # Display comparison table
    comparison_df = pd.DataFrame(comparison_data)
    st.table(comparison_df)
