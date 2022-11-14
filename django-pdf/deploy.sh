#!/bin/bash
docker build -t django-pdf:dev .
kubectl delete -f app.yaml --ignore-not-found
kubectl apply -f app.yaml
