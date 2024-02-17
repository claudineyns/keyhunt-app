FROM python:3-alpine

RUN mkdir /app && pip3 install base58 ecdsa redis

ENV INTERVAL='400000000000000000:7' \
    ADDRESS='1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU' \
    REDIS_HOST='localhost' \
    REDIS_PORT='6379'

RUN addgroup -g 1001 -S keyhunt \
 && adduser -S -G root -D -H -u 1001 keyhunt \
 && chown -R 1001 /app \
 && chgrp -R 0 /app

USER 1001

COPY --chmod=770 *.py /app

WORKDIR /app

CMD python3 keyhunt.py --interval=${INTERVAL} --address=${ADDRESS} --redis_host=$REDIS_HOST --redis_port=$REDIS_PORT
