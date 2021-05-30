import time

import requests
import json
import streamlit as st
import pandas as pd
from transformers.pipelines import pipeline

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

def answer_question():
    # Inputs
    question = st.text_input('Question')
    context = st.text_area('Context')
    model = st.text_input('Model', value="Default(distilled-bert)")

    # Execute question answering on button press
    if st.button('Answer Question'):

        payload = json.dumps({
            "question": question,
            "context": context
        })

        headers = {'Content-Type': 'application/json'}
        print(model)
        if model != "Default(distilled-bert)":
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

def answer_question_file_upload():
    uploaded_file = st.file_uploader("Choose a file", type = ['csv', 'xlsx'])

    global data
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
    menu = st.selectbox(
        "Available Models",
        model_list
    )
    if st.button('Answer Question'):

        train = df.loc[df['name'] == menu]

        model = train['model'].tolist()[0]
        print(model)
        tokenizer = train['model'].tolist()[0]
        hg_comp = pipeline('question-answering', model=model,
                           tokenizer=tokenizer)
        time.sleep(5)

        answer = []
        #model = st.text_input('Model', value="Default(distilled-bert)")

        count = 0



        for idx, row in data.iterrows():
            context = row['context']
            question = row['question']
            curr_answer = hg_comp({'question': question, 'context': context})['answer']
            answer.append(curr_answer)


            #print(answer)
    time.sleep(15)
    data["answer"] = answer
    st.title('The Answer To your Questions')
    st.table(data)
    # Inputs
    # question = st.text_input('Question')
    # context = st.text_area('Context')
    # model = st.text_input('Model', value="Default(distilled-bert)")
    #
    # # Execute question answering on button press
    # if st.button('Answer Question'):
    #
    #     payload = json.dumps({
    #         "question": question,
    #         "context": context
    #     })
    #
    #     headers = {'Content-Type': 'application/json'}
    #     print(model)
    #     if model != "Default(distilled-bert)":
    #         response = requests.request("POST", url + "answer?model="+model, headers=headers, data=payload)
    #         answer = response.json()
    #     else:
    #         response = requests.request("POST", url + "answer", headers=headers, data=payload)
    #         answer = response.json()
    #
    #
    #     value=[]
    #     value.append(answer)
    #     print(value)
    #     df = pd.DataFrame.from_dict(value, orient='columns')
    #
    #     st.title('The Answer To your Question')
    #     st.table(df)

def recent_answers():
    # Inputs
    start = st.text_input('Start Time')
    end = st.text_area('End Time')
    model = st.text_area('Model',value="None")


    # Execute question answering on button press
    if st.button('Fetch Recent Queries'):
        headers = {'Content-Type': 'application/json'}
        if model != "None":

            response = requests.request("GET", url + "answer?model=" + model + "&start=" + start + "&end=" + end,
                                        headers=headers)
            answer = response.json()
        else:
            response = requests.request("GET", url + "answer?" + "&start=" + start + "&end=" + end,
                                        headers=headers)
            answer = response.json()

        print(answer)

        df = pd.DataFrame.from_dict(answer, orient='columns')
        st.title('Recent Search Queries')
        st.table(df)


def delete_models():
    # Inputs
    model = st.text_input('Model')

    # Execute question answering on button press
    if st.button('Delete Model'):
        print(model)
        headers = {'Content-Type': 'application/json'}
        response = requests.request("DELETE", url + "models?model=" + model, headers=headers)
        print(response)
        answer = response.json()
        df = pd.DataFrame.from_dict(answer, orient='columns')

        st.title('List of Updated Models')
        st.table(df)


def get_models():
    # Inputs

    headers = {'Content-Type': 'application/json'}
    response = requests.request("GET", url + "models", headers=headers)
    print(response)
    answer = response.json()
    df = pd.DataFrame.from_dict(answer, orient='columns')

    st.title('Current Models List')
    st.table(df)


def add_models():
    # Inputs
    model_name = st.text_input('Model Name')
    model = st.text_input('Model')
    tokenizer = st.text_input('Tokenizer')

    # Execute question answering on button press
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


if __name__ == '__main__':
    st.title('Amazing Question Answering Thing!')
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
    st.sidebar.markdown("<h1>- - - - - - - - - - - - - - - - - - </h1>", unsafe_allow_html=True)
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
