FROM ubuntu:jammy
ARG APITOKEN
ARG EXTRA_INDEX_URL
ARG ES_HOST

RUN apt-get update -y
RUN apt-get install -y python3.10 python3-venv


WORKDIR ~/
RUN python3 -m venv venv

COPY pyproject.toml pyproject.toml
RUN mkdir bot
RUN bash -c "source venv/bin/activate && pip config set global.extra-index-url ${EXTRA_INDEX_URL} && pip install -e ."

COPY bot/ bot


ENV APITOKEN=${APITOKEN}
ENV ES_HOST=${ES_HOST}

CMD venv/bin/run-bot
