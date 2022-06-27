#!/bin/zsh
image=chinstrap:local
docker build -t $image . -f dockerfiles/Dockerfile
docker run --rm -v `pwd`:/chinstrap -it $image bash 