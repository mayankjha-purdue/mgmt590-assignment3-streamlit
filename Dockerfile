FROM tensorflow/tensorflow

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY webapp.py /app/webapp.py

CMD streamlit run webappe.py
