FROM mcr.microsoft.com/devcontainers/base:jammy


# run texlive in its own layer to cache it separately as it can be quite large
RUN apt-get update && apt-get install -y texlive-full

RUN apt-get update && apt-get install -y python3 python3-pip python3.10-venv

RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath
RUN pipx install poetry