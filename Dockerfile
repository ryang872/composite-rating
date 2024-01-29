# Use an official Python runtime as a parent image
# FROM python:3.8-slim-buster
FROM public.ecr.aws/lambda/python@sha256:c95e0a2af8bd2bb58e9de147305d30a6e8e598200ef4a2e9a06d14a4934fb204 as build

RUN dnf install -y unzip && \
    curl -Lo "/tmp/chromedriver-linux64.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/121.0.6167.85/linux64/chromedriver-linux64.zip" && \
    curl -Lo "/tmp/chrome-linux64.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/121.0.6167.85/linux64/chrome-linux64.zip" && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/ && \
    unzip /tmp/chrome-linux64.zip -d /opt/

FROM public.ecr.aws/lambda/python@sha256:c95e0a2af8bd2bb58e9de147305d30a6e8e598200ef4a2e9a06d14a4934fb204
    

RUN dnf install -y atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm  

### install chrome
# RUN apt-get update && apt-get install -y wget && apt-get install -y zip
# RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

### install chromedriver
# RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip \
#   && unzip chromedriver-linux64.zip && rm -dfr chromedriver_linux64.zip \
#   && mv /chromedriver-linux64/chromedriver /usr/bin/chromedriver \
#   && chmod +x /usr/bin/chromedriver


# please review all the latest versions here:
# https://googlechromelabs.github.io/chrome-for-testing/
ENV CHROMEDRIVER_VERSION=121.0.6167.85
ENV PORT=5000

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# Set the working directory in the container to /app
WORKDIR /app

# copy every content from the local file to the image
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=build /opt/chrome-linux64 /opt/chrome
COPY --from=build /opt/chromedriver-linux64 /opt/

# Make port 80 and 5000 available to the world outside this container
EXPOSE 80
EXPOSE 5000

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py" ]