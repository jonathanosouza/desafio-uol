#!/bin/bash

FILE=$1      
ORDER=$2     
OFFSET=$3 
LIMIT=$4    


if [[ "$ORDER" == "-desc" ]]; then
  sort -k1 -r "$FILE"
else
  sort -k1 "$FILE"
fi | tail -n +"$((OFFSET + 1))" | head -n "$LIMIT"
