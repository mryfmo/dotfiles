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

# The release setup.sh bootstraps: `make docker` passes the newest one at least
# 72 hours old (scripts/lib/github-release.sh) with the sha256 it verified on the host
# against the release's checksum file and GitHub release attestation. The build trusts
# only that sha256, never the release page.
ARG CHEZMOI_VERSION
ARG CHEZMOI_SHA256
# make docker rebuilds the image when this label differs from the resolved release.
LABEL chezmoi.version=$CHEZMOI_VERSION
RUN { test -n "$CHEZMOI_VERSION" && test -n "$CHEZMOI_SHA256"; } || { echo "build with --build-arg CHEZMOI_VERSION and CHEZMOI_SHA256 (make docker verifies both)" >&2; exit 1; } \
    && artifact="chezmoi_${CHEZMOI_VERSION}_linux_$(dpkg --print-architecture).tar.gz" \
    && base_url="https://github.com/twpayne/chezmoi/releases/download/v${CHEZMOI_VERSION}" \
    && cd /tmp \
    && curl -fsSLO "${base_url}/${artifact}" \
    && echo "${CHEZMOI_SHA256}  ${artifact}" | sha256sum --check --strict \
    && tar -xzf "${artifact}" chezmoi \
    && sudo install -m 0755 chezmoi /usr/local/bin/chezmoi \
    && rm -f chezmoi "${artifact}"

RUN mkdir -p ~/.local/share/fonts
RUN mkdir -p /tmp
