FROM python:3.12.4-alpine3.20

COPY . /app

WORKDIR /app

EXPOSE 8000

RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir poetry \
    && poetry install \
    mkdir music_folder

CMD ["poetry", "run", "uvicorn", "source.main:application", "--host", "0.0.0.0", "--reload"]