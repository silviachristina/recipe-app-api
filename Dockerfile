# Is the name of the image we gonna inherit from. With docker you can build a image on top of other image,  you can find a image that contains everything that you need and customized based on you project
FROM python:3.7-alpine
# Indicates who mainteing the project, you can put your name, your company name
MAINTAINER Silvia Christina    

# The away to set an environment varible on docker
# Tells python to run in a unbuffered mode witch is recommended when runs python in a Docker containers, doesn't allow python to buffer the outputs 
ENV PYTHONUNBUFFERED 1

# Install the dependencies
# Copy the requirements.txt file in our folder to the image and install using pip all the dependencies inside the requirements.txt file
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Create a directory to store the aplication source code
#  Create a folderinside the image
RUN mkdir /app
# Make the folder the default directory, any application will run starting from this location
WORKDIR /app
# Copies from our local machine to the image we created
COPY ./app /app

# Create a user that will run our application using Docker. -d means a permition to run application only. Is not reccomended running our application using the root user
RUN adduser -D user
# Switch to the user
USER user