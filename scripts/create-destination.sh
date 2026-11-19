#!/usr/bin/env bash
# Create the S3 bucket + prefix and AWS Glue database for the Iceberg destination.
# Usage: ./scripts/create-destination.sh <bucket-name> [region]
set -euo pipefail

BUCKET="${1:?Usage: $0 <bucket-name> [region]}"
REGION="${2:-us-east-1}"

echo "Creating S3 bucket s3://${BUCKET} in ${REGION}..."
if [[ "${REGION}" == "us-east-1" ]]; then
  aws s3 mb "s3://${BUCKET}" --region "${REGION}"
else
  aws s3 mb "s3://${BUCKET}" --region "${REGION}" --create-bucket-configuration "LocationConstraint=${REGION}"
fi

echo "Creating Iceberg table prefix..."
aws s3api put-object --bucket "${BUCKET}" --key market_db/market_rule/

echo "Creating Glue database market_db (if missing)..."
aws glue create-database --database-input '{"Name":"market_db"}' --region "${REGION}" 2>/dev/null \
  || echo "Glue database market_db already exists (ok)."

cat <<EOF

Next: create the Iceberg table in Athena (edit LOCATION first):
  sql/02-athena-iceberg-table.sql

Then deploy the CloudFormation stack with S3BucketName=${BUCKET}.
EOF
