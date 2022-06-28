FROM python:3.9

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y 

RUN apt install -y libsodium-dev libsecp256k1-dev libgmp-dev nodejs npm curl

RUN python3.9 -m pip install --upgrade pip

RUN pip3 install chinstrap -U --no-cache-dir

RUN chinstrap install -l -c all

ENV PATH=~/chinstrap/bin:$PATH 

WORKDIR /home

ENTRYPOINT [ "chinstrap"]