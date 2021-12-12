# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY . /code
WORKDIR /code/
RUN pip install -r requirements.txt

# Setup GDAL
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin python3-gdal

ENV SECRET_KEY=12345678
ENV DATABASE_URL=postgres://username@localhost
ENV PORT=8080
RUN chmod a+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
EXPOSE $PORT
CMD python manage.py migrate --no-input && gunicorn -b 0.0.0.0:$PORT new_school_locations.wsgi --log-file -