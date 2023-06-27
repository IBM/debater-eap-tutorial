#!/bin/bash

for (( COUNTER=0; COUNTER<150; COUNTER+=10 )); do
    bash ./warm_up_cache_eap_tutorial.sh $COUNTER 10 &
done
