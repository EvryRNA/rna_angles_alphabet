#!/bin/bash

if [ -d rna_dataset ]
then
    echo 'The rna_dataset directory already exist'
else
    git clone git@github.com:EvryRNA/my_RNAAssessment.git

    cp -r my_RNAAssessment/example/Training_set rna_dataset

    rm -rf my_RNAAssessment/
fi
