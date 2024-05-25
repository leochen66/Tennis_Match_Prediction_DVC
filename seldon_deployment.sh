#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

aws_access_key_id=$(jq -r '.AWS_ACCESS_KEY_ID' "${SCRIPT_DIR}/workflows/cert.json")
aws_secret_access_key=$(jq -r '.AWS_SECRET_ACCESS_KEY' "${SCRIPT_DIR}/workflows/cert.json")
aws_default_region=$(jq -r '.AWS_DEFAULT_REGION' "${SCRIPT_DIR}/workflows/cert.json")

# build image
s2i build "${SCRIPT_DIR}/wrapper/s2i" seldonio/seldon-core-s2i-python3:1.19.0-dev leochen66/sklearn_tennis:2.1 \
  --environment-file "${SCRIPT_DIR}/s2i_environment" \
  --env AWS_ACCESS_KEY_ID="${aws_access_key_id}" \
  --env AWS_SECRET_ACCESS_KEY="${aws_secret_access_key}" \
  --env AWS_DEFAULT_REGION="${aws_default_region}"

docker push leochen66/sklearn_tennis:2.1

# Create new Kubernetes namespace
kubectl delete namespace seldon
kubectl create namespace seldon

# apply namespace config
kubectl apply -f "${SCRIPT_DIR}/seldon_deployment.yaml"
