# start by pulling the python image
FROM python:3.6-stretch

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app
RUN pip install Flask-Bcrypt==1.0.1
RUN pip install Flask-Login==0.5.0
RUN pip install Flask-Reuploaded==1.2.0
RUN pip install Flask-WTF==1.0.1
# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["flask/app.py" ]
