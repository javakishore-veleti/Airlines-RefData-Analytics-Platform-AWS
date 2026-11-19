#!/usr/bin/env bash
# Deploy the airlines reference-data CDC CloudFormation stack.
# Usage:
#   ./scripts/deploy-stack.sh \
#     --source-endpoint-arn <arn> \
#     --source-secret-arn <arn> \
#     --subnet-group-arn <arn> \
#     --security-group-id <sg-...> \
#     --s3-bucket <bucket> \
#     [--stack-name airlines-refdata-cdc] \
#     [--region us-east-1]
set -euo pipefail

STACK_NAME="airlines-refdata-cdc"
REGION="us-east-1"
SOURCE_ENDPOINT_ARN=""
SOURCE_SECRET_ARN=""
SUBNET_GROUP_ARN=""
SECURITY_GROUP_ID=""
S3_BUCKET=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source-endpoint-arn) SOURCE_ENDPOINT_ARN="$2"; shift 2 ;;
    --source-secret-arn) SOURCE_SECRET_ARN="$2"; shift 2 ;;
    --subnet-group-arn) SUBNET_GROUP_ARN="$2"; shift 2 ;;
    --security-group-id) SECURITY_GROUP_ID="$2"; shift 2 ;;
    --s3-bucket) S3_BUCKET="$2"; shift 2 ;;
    --stack-name) STACK_NAME="$2"; shift 2 ;;
    --region) REGION="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

: "${SOURCE_ENDPOINT_ARN:?--source-endpoint-arn is required}"
: "${SOURCE_SECRET_ARN:?--source-secret-arn is required}"
: "${SUBNET_GROUP_ARN:?--subnet-group-arn is required}"
: "${SECURITY_GROUP_ID:?--security-group-id is required}"
: "${S3_BUCKET:?--s3-bucket is required}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE="${ROOT_DIR}/cloudformation/sql-to-firehose-cfn.yaml"

echo "Deploying stack ${STACK_NAME} in ${REGION}..."
aws cloudformation create-stack \
  --stack-name "${STACK_NAME}" \
  --template-body "file://${TEMPLATE}" \
  --capabilities CAPABILITY_NAMED_IAM \
  --region "${REGION}" \
  --parameters \
    "ParameterKey=DmsSourceEndpointArn,ParameterValue=${SOURCE_ENDPOINT_ARN}" \
    "ParameterKey=DmsSourceSecretArn,ParameterValue=${SOURCE_SECRET_ARN}" \
    "ParameterKey=DmsSubnetGroupArn,ParameterValue=${SUBNET_GROUP_ARN}" \
    "ParameterKey=DmsVpcSecurityGroupId,ParameterValue=${SECURITY_GROUP_ID}" \
    "ParameterKey=S3BucketName,ParameterValue=${S3_BUCKET}" \
    "ParameterKey=DmsSourceTableName,ParameterValue=market_rule" \
    "ParameterKey=GlueDatabaseName,ParameterValue=market_db" \
    "ParameterKey=GlueTableName,ParameterValue=market_rule" \
    "ParameterKey=IcebergUniqueKey,ParameterValue=rule_id"

echo "Waiting for CREATE_COMPLETE..."
aws cloudformation wait stack-create-complete \
  --stack-name "${STACK_NAME}" \
  --region "${REGION}"

aws cloudformation describe-stacks \
  --stack-name "${STACK_NAME}" \
  --region "${REGION}" \
  --query 'Stacks[0].Outputs' \
  --output table

echo "Stack ready. Start the DMS Serverless replication in the console, then validate with Athena."
