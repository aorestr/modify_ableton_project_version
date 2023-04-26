# Slim version of Python
FROM python:3.11.3-slim

COPY . /

# Download Package Information
RUN apt update

# Install Tkinter
RUN apt install -y tk

RUN pip install --upgrade pip && pip install -r /requirements.txt

# Commands to run Tkinter application
CMD ["/src/gui.py"]
ENTRYPOINT ["python3"]

# Read the above before pasting
docker run -u=$(id -u $USER):$(id -g $USER) \
           -e DISPLAY=$DISPLAY \
           -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
           -v $(pwd)/src:/src \
           --rm \
           docker_gui