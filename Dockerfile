FROM ubuntu:24.04

ARG USERNAME=mryfmo
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    git \
    sudo \
    tzdata \
    parallel \
    build-essential \
    ca-certificates

RUN existing_group="$(getent group "$USER_GID" | cut -d: -f1)" \
    && if [ -n "$existing_group" ]; then groupmod --new-name "$USERNAME" "$existing_group"; else groupadd --gid "$USER_GID" "$USERNAME"; fi \
    && existing_user="$(getent passwd "$USER_UID" | cut -d: -f1)" \
    && if [ -n "$existing_user" ]; then usermod --login "$USERNAME" --home "/home/$USERNAME" --move-home --gid "$USER_GID" "$existing_user"; else useradd --uid "$USER_UID" --gid "$USER_GID" -m "$USERNAME" -s /bin/bash; fi \
    && usermod --append --groups sudo "$USERNAME" \
    && mkdir -p "/home/$USERNAME/.local/share/chezmoi" \
    && chown -R "$USER_UID:$USER_GID" "/home/$USERNAME" \
    && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER $USERNAME
WORKDIR /home/$USERNAME/.local/share/chezmoi

RUN sudo sh -c "$(curl -fsLS get.chezmoi.io)" -- -b /usr/local/bin

RUN mkdir -p ~/.local/share/fonts
RUN mkdir -p /tmp
