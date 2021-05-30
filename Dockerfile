FROM tensorflow/tensorflow

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY answer.py /app/answer.py

CMD streamlit run webappe.py
