FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt install -y libsodium-dev libsecp256k1-dev libgmp-dev nodejs npm curl

RUN pip3 install chinstrap -U

RUN chinstrap install -l -c all

ENV PATH=~/chinstrap/bin:$PATH 

WORKDIR /home

ENTRYPOINT [ "chinstrap"]