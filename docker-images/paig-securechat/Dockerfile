FROM python:3.11.9-slim-bullseye

ARG VERSION
ARG USE_LOCAL_WHEEL

ENV APP_NAME=paig
ENV PAIG_HOME=/opt/${APP_NAME}
ENV PAIG_DEPLOYMENT=dev
ENV VERSION=$VERSION

RUN mkdir -p ${PAIG_HOME}

WORKDIR $PAIG_HOME

COPY paig_securechat-${VERSION}-py3-none-any.whl ${PAIG_HOME}

# Install paig server
RUN if [ "$USE_LOCAL_WHEEL" = "true" ] && [ -f "${PAIG_HOME}/paig_securechat-${VERSION}-py3-none-any.whl" ]; then \
        pip install "${PAIG_HOME}/paig_securechat-${VERSION}-py3-none-any.whl"; \
    else \
        pip install "paig-securechat==${VERSION}"; \
    fi

# TODO Remove below line once it is fixed in the paig-securechat
RUN sed -i "s/return self.shield_access_denied_msg, None/return str(e), None/" /usr/local/lib/python3.11/site-packages/paig_securechat/services/langchain_service_intf.py

# Install mysql dependencies
RUN pip install mysql-connector-python
RUN pip install asyncmy

# Start the server
CMD ["paig_securechat", "run", "--host", "0.0.0.0"]

