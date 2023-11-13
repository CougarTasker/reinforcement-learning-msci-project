FROM mcr.microsoft.com/devcontainers/base:jammy


# run texlive in its own layer to cache it separately as it can be quite large
RUN apt-get update && apt-get install -y texlive-full

# python setup
RUN apt-get install -y python3.10 python3-pip python3.10-venv
RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath
RUN PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install poetry

# graphics libries for kivy
RUN apt-get install -y mtdev-tools libgl1-mesa-glx

# need to be installed outside of the virtual enviroment
RUN pip install pre-commit