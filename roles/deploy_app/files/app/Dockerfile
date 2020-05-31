FROM python:3.7.6-slim-buster
ADD . /opt/query_service
WORKDIR /opt/query_service
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["python3.7", "extract_data.py"]