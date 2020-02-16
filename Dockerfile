FROM python:3.7.4

WORKDIR /usr/src/app

ENV PIPENV_COLORBLIND=1
ENV USERNAME=docker
RUN ["/usr/local/bin/pip", "install", "pipenv"]

COPY . .
RUN ["/usr/local/bin/pipenv", "sync", "--dev"]

CMD ["/usr/local/bin/pipenv", "run", "python", "word_embeddings_flow.py", "run"]
