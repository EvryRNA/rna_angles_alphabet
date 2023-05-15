FROM python:3.9
ENV LOCAL_PATH=.
WORKDIR app
COPY $LOCAL_PATH/requirements.txt .
RUN apt-get update && apt-get install bc
RUN pip install -r requirements.txt
COPY $LOCAL_PATH .
