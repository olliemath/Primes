FROM pypy:3.7-7.3.3
# RUN apt-get update && apt-get install -y python3

WORKDIR /opt/app

COPY PrimePY.py run.sh ./

ENTRYPOINT [ "./run.sh" ]
