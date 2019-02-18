FROM python:3.7-alpine

RUN apk add --no-cache ffmpeg
RUN apk --no-cache add musl-dev linux-headers g++

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV Ty 1375

WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile /code/Pipfile
RUN pipenv install --deploy --system --skip-lock --dev

ADD ./ ./

CMD ["python", "app.py"]
