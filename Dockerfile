FROM tensorflow/tensorflow

COPY requirements.txt . 

RUN pip install -r requirements.txt 

COPY webapp.py /app/webapp.py

EXPOSE 8080

CMD streamlit run /app/webapp.py --server.port 8080 --server.address=0.0.0.0 --server.enableCORS false 
