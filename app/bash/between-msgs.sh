#!/bin/bash

FILE=$1       # Arquivo
MIN=$2        # Mínimo de mensagens
MAX=$3        # Máximo de mensagens
OFFSET=$4     # Linha inicial
LIMIT=$5      # Quantidade de linhas

awk -v min="$MIN" -v max="$MAX" '$3+0 >= min && $3+0 <= max' "$FILE" | tail -n +"$((OFFSET + 1))" | head -n "$LIMIT"
