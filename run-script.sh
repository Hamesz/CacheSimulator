#!/bin/bash
optimise="False"
while getopts :f:o flag
do
    case "${flag}" in
        f) file=$OPTARG;;
        o) optimise="True";;
    esac
done
# echo "file: $file"
# echo "optimise: $optimise"

python main.py $file $optimise
