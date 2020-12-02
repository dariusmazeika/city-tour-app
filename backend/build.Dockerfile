ARG image
FROM $image

COPY . /srv/

WORKDIR /srv/
CMD ["sh", "./bin/startup.sh"]
