#!/bin/bash

# Define the target URL
TARGET_URL="http://localhost:8000"

echo "=========================================="
echo "Starting OWASP ZAP DAST Scan on $TARGET_URL"
echo "=========================================="

# Check if the app is running
if ! curl -s $TARGET_URL > /dev/null; then
    echo "Error: The application does not seem to be running at $TARGET_URL."
    echo "Please start your app first (e.g., docker-compose up or uvicorn)."
    exit 1
fi

# Create directory for reports if it doesn't exist
mkdir -p zap_reports
chmod 777 zap_reports

echo "Running ZAP Baseline Scan..."
# Use the ZAP Docker image to run a baseline scan
# -t: Target URL
# -r: Report file name (inside the container)
# -I: Fail on any warning (optional, removed here to just report)
docker run --rm \
    -v $(pwd)/zap_reports:/zap/wrk/:rw \
    --network=host \
    -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
    -t $TARGET_URL \
    -r zap_report.html \
    -I

echo "=========================================="
echo "Scan Complete!"
echo "Report saved to: zap_reports/zap_report.html"
echo "=========================================="
