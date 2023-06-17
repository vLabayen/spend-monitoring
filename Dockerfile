FROM ubuntu:jammy

RUN apt-get update -y
RUN apt-get install -y python3.10 python3-venv

WORKDIR ~/
RUN python3 -m venv venv

COPY pyproject.toml pyproject.toml
COPY bot/ bot

RUN bash -c 'source venv/bin/activate && pip install .'

CMD venv/bin/run-bot
