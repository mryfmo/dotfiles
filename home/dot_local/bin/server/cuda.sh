#!/usr/bin/env zsh

# @file home/dot_local/bin/server/cuda.sh
# @brief Export CUDA paths for server shells.
# @description
#   Sets `CUDA_HOME`, prepends the CUDA binaries to the shell path, and extends
#   `LD_LIBRARY_PATH` for CUDA libraries.
# @example
#   source ~/.local/bin/server/cuda.sh

export CUDA_HOME="/usr/local/cuda"

typeset -gU path
path=(
    $path
    ${CUDA_HOME}/bin(N-/)
)

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$CUDA_HOME/lib64"
