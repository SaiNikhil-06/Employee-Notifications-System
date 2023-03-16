FROM python:3.6.4-slim
COPY . /server02
CMD ["python","/server02/pub_sub_s2.py","s-server2"]
EXPOSE 5041
##This Dockerfile specifies a Python 3.6.4-slim base image, copies the current directory into a new directory called "server02" inside the container, sets the default command to run "pub_sub_s2.py" with the argument "s-server2" using Python, and exposes port 5041 for the container.