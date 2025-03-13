FROM python:3.11.9-slim-bullseye

ARG VERSION

ENV APP_NAME=paig
ENV PAIG_HOME=/opt/${APP_NAME}
ENV PAIG_DEPLOYMENT=dev
ENV VERSION=$VERSION

RUN mkdir -p ${PAIG_HOME}

WORKDIR $PAIG_HOME

COPY paig_securechat-${VERSION}-py3-none-any.whl ${PAIG_HOME}

# Install paig server
# RUN pip install paig-securechat==${VERSION}
RUN pip install ${PAIG_HOME}/paig_securechat-${VERSION}-py3-none-any.whl

# Install mysql dependencies
RUN pip install mysql-connector-python
RUN pip install asyncmy

# Start the server
CMD ["paig_securechat", "run", "--host", "0.0.0.0"]

