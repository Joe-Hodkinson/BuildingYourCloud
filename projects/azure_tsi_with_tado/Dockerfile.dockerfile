FROM python:3.10.1-buster
WORKDIR /usr/src/app
COPY tado.py .
RUN apt update
RUN apt install -y cmake
RUN apt install -y libxml2-dev libz-dev python-dev python3-dev build-essential
RUN pip3 install uamqp==1.5.1
RUN pip3 install nest-asyncio
RUN pip3 install azure-eventhub
CMD [ "python3", "./tado.py" ]