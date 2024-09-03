#!/bin/bash

# Create namespace for Airflow
kubectl create namespace airflow

# Install NGINX Ingress Controller
helm install nginx-ingress ingress-nginx/ingress-nginx -n airflow

# Wait for NGINX Ingress Controller to initialize (30 seconds)
echo "Waiting for NGINX Ingress Controller to initialize..."
sleep 20

# Upgrade Ingress Controller to use NodePort service
helm upgrade nginx-ingress ingress-nginx/ingress-nginx -n airflow --set controller.service.type=NodePort
sleep 20

# Apply Persistent Volume and Persistent Volume Claim settings
kubectl apply -f AF-pv_pvc_setting.yaml -n airflow

# Create secrets for Airflow
kubectl create secret generic airflow-secrets --from-env-file=.env -n airflow

# Wait for secrets to be created (10 seconds)
echo "Waiting for secrets to be created..."

# Install Airflow using Helm
helm install test oci://registry-1.docker.io/bitnamicharts/airflow -f values.yaml -n airflow

# Wait for Airflow to initialize (60 seconds)
echo "Waiting for Airflow to initialize..."
sleep 90

echo "Airflow deployment initiated. Please wait for all pods to be up and running."
