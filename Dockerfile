FROM ubuntu
MAINTAINER Brandon Scott

RUN apt update -y -q
RUN apt install -y -q git python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install twython
RUN pip3 install pillow

CMD ["python3", "/bot/PollingService.py"]

# docker build -t ImgShfl ~/ImgShfl/
# docker run --name ImgShfl --restart=always --log-opt max-size=100k -v /home/brandon/ImgShfl/:/bot/ -d ImgShfl