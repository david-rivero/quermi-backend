#!/bin/bash
# Run setup.sh with . (. setup.sh)

eval ". env/bin/activate"

for i in $(cat variables.env); do
    var_name=$(echo $i | cut -d"=" -f1)
    var_value=$(echo $i | cut -d"=" -f2)

    export $var_name=$var_value;
done

