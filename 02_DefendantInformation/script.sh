#!/bin/bash

# Get all named defendants of the case
python3 named_defendants.py

# Predict demographic information given name
Rscript demographics.R