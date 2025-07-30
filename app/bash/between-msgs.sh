#!/bin/bash

FILE=$1       
MIN=$2        
MAX=$3        
OFFSET=$4     
LIMIT=$5      

awk -v min="$MIN" -v max="$MAX" '$3+0 >= min && $3+0 <= max' "$FILE" | tail -n +"$((OFFSET + 1))" | head -n "$LIMIT"
