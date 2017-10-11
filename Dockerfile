FROM hypriot/rpi-alpine-scratch

RUN apk update && apk upgrade && apk add bash 
RUN apk add python3

RUN rm -rf /var/cache/apk/*

RUN mkdir /code
 WORKDIR /code
 ADD code/requirements.txt /code/
 RUN pip3 install -r requirements.txt
 ADD code /code/
CMD ["/bin/bash"]
