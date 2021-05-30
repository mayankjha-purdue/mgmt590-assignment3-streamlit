FROM tensorflow/tensorflow

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY webapp.py /app/webapp.py

EXPOSE 8080

CMD streamlit run --server.port 8080 --server.enableCORS false /app/webapp.py
