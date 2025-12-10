#!/bin/bash

# GitHub Secrets Copy Helper Script
# This script helps copy each secret value to clipboard for easy pasting into GitHub

set -e

echo "======================================"
echo "GitHub Secrets Copy Helper"
echo "======================================"
echo ""
echo "This script will copy each secret value to your clipboard."
echo "After copying, paste it into GitHub:"
echo "  https://github.com/tchaas/tchaasledger/settings/secrets/actions/new"
echo ""
echo "Press ENTER to start..."
read

# Secret 1: GCP_SA_KEY
echo ""
echo "------------------------------------"
echo "Secret 1/5: GCP_SA_KEY"
echo "------------------------------------"
echo "Description: Service account JSON key for GitHub Actions"
echo ""
echo "Press ENTER to copy to clipboard..."
read
cat /Users/tchaasalexander-wright/tchaas-ledger-990/github-actions-key.json | pbcopy
echo "✅ GCP_SA_KEY copied to clipboard!"
echo ""
echo "Now:"
echo "  1. Go to GitHub → Settings → Secrets and variables → Actions"
echo "  2. Click 'New repository secret'"
echo "  3. Name: GCP_SA_KEY"
echo "  4. Value: CMD+V to paste"
echo "  5. Click 'Add secret'"
echo ""
echo "Press ENTER when done..."
read

# Secret 2: DATABASE_URL
echo ""
echo "------------------------------------"
echo "Secret 2/5: DATABASE_URL"
echo "------------------------------------"
echo "Description: PostgreSQL connection string"
echo "Value: postgresql://localhost/tchaas_ledger (placeholder)"
echo ""
echo "Press ENTER to copy to clipboard..."
read
echo -n "postgresql://localhost/tchaas_ledger" | pbcopy
echo "✅ DATABASE_URL copied to clipboard!"
echo ""
echo "Now:"
echo "  1. Click 'New repository secret'"
echo "  2. Name: DATABASE_URL"
echo "  3. Value: CMD+V to paste"
echo "  4. Click 'Add secret'"
echo ""
echo "Press ENTER when done..."
read

# Secret 3: SECRET_KEY
echo ""
echo "------------------------------------"
echo "Secret 3/5: SECRET_KEY"
echo "------------------------------------"
echo "Description: Flask secret key for sessions"
echo "Value: 72565073b0bc0250bd8b0374ce8ab7f466891fc509ff6c2cbc728c5264f9315b"
echo ""
echo "Press ENTER to copy to clipboard..."
read
echo -n "72565073b0bc0250bd8b0374ce8ab7f466891fc509ff6c2cbc728c5264f9315b" | pbcopy
echo "✅ SECRET_KEY copied to clipboard!"
echo ""
echo "Now:"
echo "  1. Click 'New repository secret'"
echo "  2. Name: SECRET_KEY"
echo "  3. Value: CMD+V to paste"
echo "  4. Click 'Add secret'"
echo ""
echo "Press ENTER when done..."
read

# Secret 4: CLOUD_SQL_INSTANCE
echo ""
echo "------------------------------------"
echo "Secret 4/5: CLOUD_SQL_INSTANCE"
echo "------------------------------------"
echo "Description: Cloud SQL instance connection name"
echo "Value: tchaas-ledger:us-central1:tchaas-ledger-db (placeholder)"
echo ""
echo "Press ENTER to copy to clipboard..."
read
echo -n "tchaas-ledger:us-central1:tchaas-ledger-db" | pbcopy
echo "✅ CLOUD_SQL_INSTANCE copied to clipboard!"
echo ""
echo "Now:"
echo "  1. Click 'New repository secret'"
echo "  2. Name: CLOUD_SQL_INSTANCE"
echo "  3. Value: CMD+V to paste"
echo "  4. Click 'Add secret'"
echo ""
echo "Press ENTER when done..."
read

# Secret 5: BACKEND_API_URL
echo ""
echo "------------------------------------"
echo "Secret 5/5: BACKEND_API_URL"
echo "------------------------------------"
echo "Description: Backend API URL for frontend"
echo "Value: https://api.tchaas-ledger.com (placeholder)"
echo ""
echo "Press ENTER to copy to clipboard..."
read
echo -n "https://api.tchaas-ledger.com" | pbcopy
echo "✅ BACKEND_API_URL copied to clipboard!"
echo ""
echo "Now:"
echo "  1. Click 'New repository secret'"
echo "  2. Name: BACKEND_API_URL"
echo "  3. Value: CMD+V to paste"
echo "  4. Click 'Add secret'"
echo ""
echo "Press ENTER when done..."
read

# Completion
echo ""
echo "======================================"
echo "✅ All secrets copied!"
echo "======================================"
echo ""
echo "Verification:"
echo "  - Go to https://github.com/tchaas/tchaasledger/settings/secrets/actions"
echo "  - You should see 5 secrets listed"
echo ""
echo "Next steps:"
echo "  1. Test CI/CD by pushing a commit:"
echo "     cd /Users/tchaasalexander-wright/tchaas-ledger-990"
echo "     git add ."
echo "     git commit -m 'test: trigger CI/CD workflows'"
echo "     git push origin main"
echo ""
echo "  2. Monitor workflows:"
echo "     https://github.com/tchaas/tchaasledger/actions"
echo ""
echo "  3. After successful deployment, update these secrets with real values:"
echo "     - DATABASE_URL (after Cloud SQL setup)"
echo "     - CLOUD_SQL_INSTANCE (after Cloud SQL setup)"
echo "     - BACKEND_API_URL (after first backend deployment)"
echo ""
echo "  4. Delete local service account key:"
echo "     rm /Users/tchaasalexander-wright/tchaas-ledger-990/github-actions-key.json"
echo ""
echo "Documentation:"
echo "  - GITHUB_SECRETS_SETUP.md - Detailed instructions"
echo "  - CICD_SETUP_COMPLETE.md - Complete setup summary"
echo "  - docs/deployment/CI_CD_SETUP.md - CI/CD reference"
echo ""
