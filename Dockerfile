# python version
FROM python:3.13.5-slim

# install package untuk container
RUN apt-get update && apt-get install -y \
    libreoffice ffmpeg \           
    && rm -rf /var/lib/apt/lists/*

# buat workdir
WORKDIR /app

# copy file local ke docker
COPY . .

# install uv & library
RUN pip install --no-cache-dir uv && \
    uv venv

# ambil execute py
ENV PATH=".venv/bin:$PATH"

# sync toml to .venv
RUN uv sync

# running bot
CMD [ "uv",  "run", 'main.py']