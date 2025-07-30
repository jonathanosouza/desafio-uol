#!/bin/bash

FILE=$1
MODE=$2

if [[ "$MODE" == "-min" ]]; then
  sort -k5 "$FILE" | head -n 1
else
  sort -k5 "$FILE" | tail -n 1
fi
