FROM ubuntu:24.04

ARG USERNAME=mryfmo
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# python3 runs the chezmoi modify scripts of the Codex and Claude configs and scripts/check-agent-runtime.py
# (make apply-check). The apt step carries two bounds (U610). apt's own options, the bounds the runner's apt gets
# (scripts/ci/drop-azure-apt-mirror.py, tests/unit/test_apt_mirror.py), are idle bounds: a connection or read silent
# for 15 s is given up and retried three times, so a stalled archive.ubuntu.com fails the layer fast. A mirror that
# keeps trickling bytes never trips them (runs 44475635634 and 44497689181: 105 MB at under 100 KB/s, the job
# cancelled at its 15 minutes), so the whole step also runs under coreutils timeout, a total bound of 600 s, inside
# the timeout-minutes of .github/workflows/apply-check.yml: the layer fails and the job's rerun or the cached layer
# takes over, instead of the job being cancelled. APT_WEEK is the ISO week of the build (date -u +%G-W%V, passed by
# make docker-image and printed by make docker-build-args), declared right before the step: every RUN after an ARG
# uses it implicitly (Docker Docs, ARG, impact on build caching), so the layer's cache key changes weekly and a
# cached apt layer carries packages at most a week older than a cold build's.
ARG APT_WEEK
RUN timeout 600 sh -c 'apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 update && \
    apt-get -o Acquire::http::Timeout=15 -o Acquire::Retries=3 install -y --no-install-recommends \
    curl \
    git \
    sudo \
    tzdata \
    parallel \
    build-essential \
    ca-certificates \
    python3'

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
ARG DOCKERFILE_ID
# make docker-image rebuilds the image when the version label differs from the resolved release,
# when the sha256 label of a host-verified archive is missing, or when the image was built from
# another Dockerfile (DOCKERFILE_ID is its git blob id).
LABEL chezmoi.version=$CHEZMOI_VERSION chezmoi.sha256=$CHEZMOI_SHA256 dotfiles.dockerfile=$DOCKERFILE_ID
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
