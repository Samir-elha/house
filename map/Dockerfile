FROM ubuntu:16.04
# Update and install python
RUN apt-get update -y && \
    apt-get install -y python3-pip python3 && apt-get -y install locales

# create folder 
RUN mkdir /app
ADD . /app
WORKDIR /app

# Install fing
RUN dpkg -i files/fing-5.5.2-amd64.deb

# Upgrade pip to version 21
RUN pip3 install --upgrade "pip < 21.0" 

#install requirements
RUN pip3 install -r requirements.txt

#variable for starting
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8 

# flask variables
ENV FLASK_APP=house
ENV FLASK_DEBUG=1

# run flask
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"] 