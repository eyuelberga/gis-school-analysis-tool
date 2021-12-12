# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY . /code
WORKDIR /code/
RUN pip install -r requirements.txt

ENV SECRET_KEY=

# Setup GDAL
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin python3-gdal

ENV SECRET_KEY=12345678
ENV DATABASE_URL=postgres://username@localhost
RUN chmod a+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
EXPOSE 8000
CMD python manage.py migrate --no-input && gunicorn -b 0.0.0.0:8000 new_school_locations.wsgi --log-file -