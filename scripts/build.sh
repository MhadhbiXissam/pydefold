#!/bin/bash
set -euo pipefail
file_path=
version=1.11.1
git_root=$(git rev-parse --show-toplevel)

# Pushd to git root
pushd "$git_root" 
[ -d ".tmp" ] && rm -rf ".tmp"
mkdir .tmp
pushd .tmp
git clone -b $version  https://github.com/MhadhbiXissam/defold-protos.git 
popd
pydefold=defoldsdk
[ -d "$pydefold" ] && rm -rf "$pydefold"
mkdir $pydefold
protoc=".tmp/defold-protos/bin/x86_64-linux/protoc"
proto_folder=.tmp/defold-protos/defold-sdk

$protoc -I "./$proto_folder" --python_out="$pydefold" --include_imports  ./"$proto_folder"/**/*.proto
rm -rf .tmp
python scripts/clean.py
python Test.py

find "$pydefold" -type d -name "__pycache__" -exec rm -rf {} +
popd 
