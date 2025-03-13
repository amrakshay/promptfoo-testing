FROM python:3.11.9-slim-bullseye

ARG VERSION

ENV APP_NAME=paig
ENV PAIG_HOME=/opt/${APP_NAME}
ENV PAIG_DEPLOYMENT=dev
ENV VERSION=$VERSION

RUN mkdir -p ${PAIG_HOME}

WORKDIR $PAIG_HOME

COPY ./paig_server-${VERSION}-py3-none-any.whl ${PAIG_HOME}/

# Install paig server
# RUN pip install paig-server==${VERSION}
RUN pip install ${PAIG_HOME}/paig_server-${VERSION}-py3-none-any.whl
RUN python -m spacy download en_core_web_lg

# Install mysql dependencies
RUN pip install mysql-connector-python
RUN pip install asyncmy

RUN apt-get update && apt-get install vim -y

# Start the server
CMD ["paig", "run", "--host", "0.0.0.0"]

