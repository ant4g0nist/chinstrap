FROM python:3

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt install -y libsodium-dev libsecp256k1-dev libgmp-dev nodejs
RUN pip3 install chinstrap -U

WORKDIR /home

ENTRYPOINT [ "bash" ]