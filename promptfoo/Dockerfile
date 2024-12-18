FROM node:latest

ENV APP_NAME=promptfoo
ENV PROMPTFOO_HOME=/opt/${APP_NAME}

RUN mkdir -p ${PROMPTFOO_HOME}
RUN mkdir -p ${PROMPTFOO_HOME}/data

WORKDIR $PROMPTFOO_HOME

# Install promptfoo
RUN npm install -g promptfoo

# Install vim
RUN apt-get update && apt-get install -y vim
RUN apt-get install -y python3-requests

WORKDIR $PROMPTFOO_HOME/data

# Start the environment
CMD ["tail", "-f", "/dev/null"]

