FROM python:3.11-slim
WORKDIR /srv

COPY pyproject.toml requirements.txt /srv/
COPY src /srv/src
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir .

COPY . /srv
EXPOSE 8000
