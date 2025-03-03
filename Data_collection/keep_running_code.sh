#!/bin/bash

until /Users/colineritz/Desktop/document_master_project/Code/data_collection/Data_collection_python_package/capture_to_Googlecloud.py

do
    currenttime=$(date +%H:%M)
    if [[ "$currenttime" > "09:30" ]] || [[ "$currenttime" < "23:30" ]]; then
        sleep 300
        echo "Restarting"
    else
        sleep 1800
        echo "Restarting"
    fi
    
done

   