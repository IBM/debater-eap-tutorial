#!/bin/bash
ApiKeysArray=("" "")

# $1 index to start
# $2 how many to take
ApiKeysArray=("${ApiKeysArray[@]:$1:$2}")

for val1 in ${ApiKeysArray[*]}; do
     echo 'running on api_key:'  $val1
     env DEBATER_API_KEY=$val1 jupyter nbconvert --to notebook --ExecutePreprocessor.kernel_name=kpa_env --execute austin_demo_with_answers.ipynb
done
