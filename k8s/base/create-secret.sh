#!/bin/bash

# Script untuk create Kubernetes Secret untuk Tuya Alarm
# Usage: ./create-secret.sh [namespace]

set -e

# Default namespace
NAMESPACE=${1:-production}

echo "Creating secret 'tuya-alarm-secrets' in namespace '${NAMESPACE}'"

# Prompt untuk credentials (atau bisa read dari .env)
read -p "Enter TUYA_ACCESS_ID: " TUYA_ACCESS_ID
read -sp "Enter TUYA_ACCESS_SECRET: " TUYA_ACCESS_SECRET
echo ""
read -p "Enter TUYA_ENDPOINT [https://openapi-sg.iotbing.com]: " TUYA_ENDPOINT
TUYA_ENDPOINT=${TUYA_ENDPOINT:-https://openapi-sg.iotbing.com}

read -p "Enter FLASK_HOST [0.0.0.0]: " FLASK_HOST
FLASK_HOST=${FLASK_HOST:-0.0.0.0}

read -p "Enter FLASK_PORT [5000]: " FLASK_PORT
FLASK_PORT=${FLASK_PORT:-5000}

read -p "Enter FLASK_DEBUG [False]: " FLASK_DEBUG
FLASK_DEBUG=${FLASK_DEBUG:-False}

read -p "Enter LOG_LEVEL [INFO]: " LOG_LEVEL
LOG_LEVEL=${LOG_LEVEL:-INFO}

# Create namespace if not exists
kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

# Create secret
kubectl create secret generic tuya-alarm-secrets \
  --namespace=${NAMESPACE} \
  --from-literal=tuya-access-id="${TUYA_ACCESS_ID}" \
  --from-literal=tuya-access-secret="${TUYA_ACCESS_SECRET}" \
  --from-literal=tuya-endpoint="${TUYA_ENDPOINT}" \
  --from-literal=flask-host="${FLASK_HOST}" \
  --from-literal=flask-port="${FLASK_PORT}" \
  --from-literal=flask-debug="${FLASK_DEBUG}" \
  --from-literal=log-level="${LOG_LEVEL}" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "Secret created successfully in namespace '${NAMESPACE}'"
echo ""
echo "To verify:"
echo "  kubectl get secret tuya-alarm-secrets -n ${NAMESPACE}"
echo ""
echo "To view (WARNING: shows credentials):"
echo "  kubectl get secret tuya-alarm-secrets -n ${NAMESPACE} -o yaml"