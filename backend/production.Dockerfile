ARG IMAGE=base
FROM python:alpine as base

ENV PYTHONUNBUFFERED 1
EXPOSE 8000 8000

# Add runtime dependencies
RUN apk add --no-cache libpq libxslt libjpeg zlib jpeg bash postgresql-client geos gdal binutils

COPY requirements.txt .

RUN apk add --no-cache --virtual build-deps gcc musl-dev postgresql-dev libxslt-dev jpeg-dev libffi-dev git rust cargo \
	&& pip install --no-cache-dir pip-tools \
	&& pip-sync \
	&& apk --purge del build-deps

RUN ln -s $(find /usr/lib -name libgdal* | head -n 1) /usr/lib/libgdal.so \
	&& ln -s /usr/lib/libgeos_c.so.1 /usr/lib/libgeos_c.so

RUN rm -f requirements.txt

FROM $IMAGE as build

RUN mkdir /app
COPY . /app/
WORKDIR /app/
CMD ["sh", "./bin/startup.sh"]
