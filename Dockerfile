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
# Uses the package name that comes with alpine, apk is the name of the package, update before install, and --no-cache means don't install the registry index on your docker file, is best practice, don't include any extra dependencies,  
RUN apk add --update --no-cache postgresql-client jpeg-dev
# --virtual setup a alias for you dependencies to easily remove later
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
# Now delete the dependencies 
RUN apk del .tmp-build-deps

# Create a directory to store the aplication source code
#  Create a folderinside the image
RUN mkdir /app
# Make the folder the default directory, any application will run starting from this location
WORKDIR /app
# Copies from our local machine to the image we created
COPY ./app /app

# Create directory to store all user files, such as fotos, images, etc
# -p create each folder if it doesn't exists
# This directory will be share to other containers, will be used to transfer the files to a web server repository
RUN mkdir -p /vol/web/media
# Create directory to store all the static content, js, css, files
RUN mkdir -p /vol/web/static
# Create a user that will run our application using Docker. -d means a permition to run application only. Is not reccomended running our application using the root user
RUN adduser -D user
# Sets the ownership of the of the directory 
# -R means recursive, wich sets all the directories to the user after the /vol/
RUN chown -R user:user /vol/
# Give permissions - user can do everything rest can read and execute 
RUN chmod -R 755 /vol/web
# Switch to the user
USER user