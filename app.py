# set the huggingface api token as envinorment variable

import os
from secret_api_keys import huggingface_api_key
os.environ['HUGGINGFACEHUB_API_TOKEN'] = huggingface_api_key

# importing the huggingface endpoint
from langchain_huggingface import HuggingFaceEndpoint
llm = HuggingFaceEndpoint (
repo_id = 'meta-llama/Meta-Llama-3-8B-Instruct',
token = huggingface_api_key,
temperature = 0.6
)

# define a promtTemplate for title suggestions
from langchain.prompts import PromptTemplate # importing promptTemplate Class from Langchain

prompt_Template_for_title_suggestion = PromptTemplate(
    input_variables = ['topic'], #specifying the input variables 
    template = #Defining the prompt template 

    '''
    I'm planning a blog post on topic : {topic} .
    The Title is informative , or humorous, or presuasive.
    The Target audience are beginners , tech enthusiasts.
    suggest list of ten creative and attention-grabbing titles for this blog post
    Don't give explanation or overview for each title.
    '''
)

#define a template for blog generation

prompt_Template_for_Blog = PromptTemplate(
    inputvariables = ['title,keywords,Blog_Length'],
    template = 

    '''
    Write a high-Quality , informative , Technical blog post on topic {title}

    Target the content towards a begginer auidence.

    use a conversational writing style and structure the content with introduction , body paragraphs and conclusion.

    Try to incoperate these words : {keywords}.

    Aim for a content length of : {Blog_Length}.

    Make the content engaging and capture the reader's attention.
    '''
)

#creating the chains 
title_suggestion_chain = prompt_Template_for_title_suggestion | llm
blog_chain = prompt_Template_for_Blog | llm

#Desiging the user interface
import streamlit as st
st.title('AI BLOG Content Assistant....')
st.subheader('Create High-Quality Blog Content without breaking the bank')

#Feature - 1.Title Generation
st.subheader('Title Generator')
topic_expander = st.expander('Input the topic') 

with topic_expander:
    topic_name = st.text_input('',key='topic_name')
    button = st.button('submit the topic')

    if button:
        st.write(title_suggestion_chain.invoke({topic_name}))

#Feature - 2. Blog Generation

st.subheader('Blog Generation')
Blog_expander = st.expander('Input Blog Details')

with Blog_expander:
    Title_of_the_blog = st.text_input('Enter the title',key='title_name')
    num_of_words = st.slider('Number of words',min_value=50,max_value=1000,step=50)
    
    if 'keywords' not in st.session_state: 
        st.session_state['keywords'] = []  # Initialize as an empty list if not present

keywords_input = st.text_input('Enter a Keyword: ')  # Input Field for adding keywords
keywords_button = st.button('Add Keyword')  # Button for adding keywords

if keywords_button: 
    if keywords_input.strip():  # Ensure the input is not empty or only spaces
        st.session_state['keywords'].append(keywords_input.strip())  # Add keyword to the list
        keywords_input = ''  # Clear the keyword input field

# Display the current list of keywords
for keyword in st.session_state['keywords']:
    st.write(f"<div style='display: inline-block; background-color: lightgray; padding: 5px; margin: 5px;'>{keyword}</div>", unsafe_allow_html=True)

button_blog = st.button('Submit The Info')

if button_blog:
    formatted_words = []
    for i in st.session_state['keywords']:
        if i:  # Ensure `i` is not None or empty
            formatted_words.append(i.lstrip('0123456789: ').strip('"').strip("'"))
    formatted_words = ', '.join(formatted_words)

    st.subheader(Title_of_the_blog)
    st.write(blog_chain.invoke({'title': Title_of_the_blog, 'keywords': formatted_words, 'Blog_Length': num_of_words}))
