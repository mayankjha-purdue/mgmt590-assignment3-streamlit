#--------------------------------------------------------------#
# Web application to perform tasks on the Question Answer -API #
#--------------------------------------------------------------#

#-----------------------#
# Import the Libraries  #
#-----------------------#
import time
import requests
import json
import streamlit as st
import pandas as pd
from transformers.pipelines import pipeline


#-----------------------------------------#
# Calling the Question Answering REST API #
#-----------------------------------------#
url = "https://mgmt590-assignment3-flask-flmzcdy22a-uc.a.run.app/"

def flatten_dict(d):
    """ Returns list of lists from given dictionary """
    l = []
    for k, v in sorted(d.items()):
        if isinstance(v, dict):
            flatten_v = flatten_dict(v)
            for my_l in reversed(flatten_v):
                my_l.insert(0, k)

            l.extend(flatten_v)

        elif isinstance(v, list):
            for l_val in v:
                l.append([k, l_val])

        else:
            l.append([k, v])

    return l

#------------------------------------------------------------------#
# Function to get the answers when given a question and a context  #
#------------------------------------------------------------------#
def answer_question():
    # Input the question
    question = st.text_input('Question')
    # Input the context
    context = st.text_area('Context')
    headers = {'Content-Type': 'application/json'}
    # Get the response with a GET request from the API
    response = requests.request("GET", url + "models", headers=headers)
    print(response)
    answer = response.json()
    df = pd.DataFrame.from_dict(answer, orient='columns')
    # Appending the list of models
    model_list = df["name"].tolist()
    model = None
    # Check box for optional inputs
    if st.checkbox('Choose a Model (optional)'):
        model = st.selectbox(
            "Available Models",
            model_list
        )
    # Execute question answering on button press
    if st.button('Answer Question'):
        payload = json.dumps({
            "question": question,
            "context": context
        })
        headers = {'Content-Type': 'application/json'}
        print(model)
    # Model is an optional input parameter
    # Loading default model if model parameter is not given
    # Get the answer from a POST request to the API
        if model != None:

            response = requests.request("POST", url + "answer?model="+model, headers=headers, data=payload)
            answer = response.json()
        else:
            response = requests.request("POST", url + "answer", headers=headers, data=payload)
            answer = response.json()

        value=[]
        value.append(answer)
        print(value)
        df = pd.DataFrame.from_dict(value, orient='columns')
        st.title('The Answer To your Question')
        st.table(df)

#--------------------------------------------------------------------------------------#
# Function to get the answers if a file is uploaded with question and context columns  #
#--------------------------------------------------------------------------------------#
def answer_question_file_upload():
    # Uploading the file
    uploaded_file = st.file_uploader("Choose a file", type = ['csv', 'xlsx'])
    global data
    # Check for an empty file and throw an exception fo an empty file
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)

        except Exception as e:
            print(e)
            data = pd.read_excel(uploaded_file)
    time.sleep(5)
    if st.button("Load Data"):
        # Raw data
        st.dataframe(data)
    time.sleep(5)
    headers = {'Content-Type': 'application/json'}
    response = requests.request("GET", url + "models", headers=headers)
    print(response)
    answer = response.json()
    df = pd.DataFrame.from_dict(answer, orient='columns')
    model_list = df["name"].tolist()
    menu = "distilled-bert"

    # Choose a model
    if st.checkbox('Choose a Model(optional)'):
        menu = st.selectbox(
            "Available Models",
            model_list
        )
    # Button to answer a question
    if st.button('Answer Question'):
        # Match the model input
        # Model name
        train = df.loc[df['name'] == menu]
        # Model type
        model = train['model'].tolist()[0]
        print(model)
        # Tokenizer
        tokenizer = train['model'].tolist()[0]
        #TRaining the model
        hg_comp = pipeline('question-answering', model=model,
                           tokenizer=tokenizer)
        answer = []
        count = 0
        # Output the answers
        for idx, row in data.iterrows():
            context = row['context']
            question = row['question']
            curr_answer = hg_comp({'question': question, 'context': context})['answer']
            answer.append(curr_answer)

# Display output
    time.sleep(15)
    data["answer"] = answer
    st.title('The Answers To your Questions')
    st.table(data)

#-------------------------------------------------#
# Function to get the recently answered questions #
#-------------------------------------------------#
# Optional Inputs : Model Name
# Mandatory Inputs : Start Time and End Time (Unix timestamp)
def recent_answers():
    # Inputs
    start = st.text_input("Start Time (UNIX Time) e.g. 1622765112")
    end = st.text_area("End Time (UNIX Time) e.g. 1622765114")
    headers = {'Content-Type': 'application/json'}
    # GET request to the API for model details
    response = requests.request("GET", url + "models", headers=headers)
    print(response)
    answer = response.json()
    df = pd.DataFrame.from_dict(answer, orient='columns')
    model_list = df["name"].tolist()
    model = None
    # Optional input : Model Name
    if st.checkbox('Choose a Model(optional)'):
        model = st.selectbox(
            "Available Models",
            model_list
        )
    # Execute question answering on button press
    if st.button('Fetch Recent Queries'):
        headers = {'Content-Type': 'application/json'}

        # Passing the default values if the model is not selected
        if model != None:
            response = requests.request("GET", url + "answer?model=" + model + "&start=" + start + "&end=" + end,
                                        headers=headers)
            answer = response.json()
        # Passing the input model details
        else:
            response = requests.request("GET", url + "answer?" + "&start=" + start + "&end=" + end,
                                        headers=headers)
            answer = response.json()

        print(answer)
# Display the output
        df = pd.DataFrame.from_dict(answer, orient='columns')
        st.title('Recent Search Queries')
        st.table(df)

#------------------------------#
# Function to delete a model   #
#------------------------------#
def delete_models():
    # Inputs
    headers = {'Content-Type': 'application/json'}
    response = requests.request("GET", url + "models", headers=headers)
    print(response)
    answer = response.json()
    df = pd.DataFrame.from_dict(answer, orient='columns')
    model_list = df["name"].tolist()
    model_list = model_list[1:]

    model = None
    # Constraint to not delete the default model
    if st.checkbox("Choose a Model (You can't delete the Default Model)"):
        model = st.selectbox(
            "Available Models",
            model_list
        )
    # Execute question answering on button press
    if st.button('Delete a Model'):
        print(model)
        headers = {'Content-Type': 'application/json'}
        # Call the REST API using the DELETE method
        response = requests.request("DELETE", url + "models?model=" + model, headers=headers)
        print(response)
        answer = response.json()
        df = pd.DataFrame.from_dict(answer, orient='columns')
# Display Output
        st.title('List of Updated Models')
        st.table(df)

#----------------------------------------------------#
# Get the list of available models in the database   #
#----------------------------------------------------#
def get_models():
    # Inputs
    headers = {'Content-Type': 'application/json'}
    response = requests.request("GET", url + "models", headers=headers)
    print(response)
    answer = response.json()
    df = pd.DataFrame.from_dict(answer, orient='columns')

    st.title('Current List of Models')
    st.table(df)

#-------------------------------------------#
# Function to Add a model to the database   #
#-------------------------------------------#
def add_models():
    # Inputs
    model_name = st.text_input('Model Name e.g. distilled-bert')
    model = st.text_input('Model e.g. distilbert-base-uncased-distilled-squad')
    tokenizer = st.text_input('Tokenizer e.g. distilbert-base-uncased-distilled-squad')

    # Execute question answering on button press
    try:
        if st.button('Add Model'):
            payload = json.dumps({
                "name": model_name,
                "model": model,
                "tokenizer": tokenizer
            })
            headers = {'Content-Type': 'application/json'}
            response = requests.request("PUT", url + "models", headers=headers, data=payload)
            print(response)
            answer = response.json()
            df = pd.DataFrame.from_dict(answer, orient='columns')

            st.title('List of Updated Models')
            st.table(df)
    except:
        st.text("Input a valid Model Name/Tokenizer")

# This runs by default
if __name__ == '__main__':
    st.title('Amazing Question Answering App!')
    lijst = [
        "List Available Models",
        "Add a Model",
        "Delete a Model",
        "Answer a Question",
        "List Recently Answered Questions",
        "File Upload"
    ]
    st.sidebar.header("Choose an Option")
    menu_keuze = st.sidebar.selectbox(
        "",
        lijst,
        index=0,
    )
    st.sidebar.markdown("<h1>- - - - - - - - - - - - - - - - - - - -</h1>", unsafe_allow_html=True)
    if menu_keuze == "List Available Models":
        get_models()

    elif menu_keuze == "Add a Model":
        add_models()

    elif menu_keuze == "Delete a Model":
        delete_models()

    elif menu_keuze == "Answer a Question":
        answer_question()

    elif menu_keuze == "List Recently Answered Questions":
        recent_answers()

    elif menu_keuze == "File Upload":
        answer_question_file_upload()

