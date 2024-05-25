FROM python:3.11.6-slim-bullseye
ENV DOCKER_OVERRIDE=1
ENV PROJECT_DIR=/app

WORKDIR ${PROJECT_DIR}
COPY . .


# installing pip requirements
RUN pip install -U pip && \
    pip install -U setuptools && \
    pip install -r requirements.txt

# running django server
CMD [ "python", "manage.py", "runserver", "0:8000" ]
