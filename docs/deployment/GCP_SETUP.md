# GCP Setup Guide for Tchaas Ledger 990

## Project Information

- **Project ID**: `tchaas-ledger`
- **Project Number**: `1057248865206`
- **Project Name**: Tchaas-ledger

## Enabled APIs

✅ Cloud Monitoring API
✅ Cloud SQL Admin API
✅ Cloud Run API

## Local Development Setup

### 1. Set Active Project

```bash
gcloud config set project tchaas-ledger
```

### 2. Authenticate

```bash
# Application default credentials (for local development)
gcloud auth application-default login

# User credentials
gcloud auth login
```

### 3. Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cd ~/tchaas-ledger-990/backend
cp .env.example .env
```

Edit `.env`:
```env
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=your-secret-key-change-this
DATABASE_URL=postgresql://localhost/tchaas_ledger
GCP_PROJECT_ID=tchaas-ledger
ENABLE_MONITORING=true
ENABLE_GCP_MONITORING=false  # Set to true when deploying to GCP
```

## Cloud SQL Setup (for Production)

### Create Cloud SQL Instance

```bash
# Create PostgreSQL instance
gcloud sql instances create tchaas-ledger-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1 \
    --project=tchaas-ledger

# Set root password
gcloud sql users set-password postgres \
    --instance=tchaas-ledger-db \
    --password=YOUR_SECURE_PASSWORD
```

### Create Database

```bash
gcloud sql databases create tchaas_ledger \
    --instance=tchaas-ledger-db
```

### Get Connection Name

```bash
gcloud sql instances describe tchaas-ledger-db \
    --format='value(connectionName)'
```

This will output something like: `tchaas-ledger:us-central1:tchaas-ledger-db`

## Cloud Run Setup (for Production)

### Build and Deploy

```bash
cd ~/tchaas-ledger-990

# Build container
gcloud builds submit --tag gcr.io/tchaas-ledger/tchaas-ledger-api

# Deploy to Cloud Run
gcloud run deploy tchaas-ledger-api \
    --image gcr.io/tchaas-ledger/tchaas-ledger-api \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --add-cloudsql-instances tchaas-ledger:us-central1:tchaas-ledger-db \
    --set-env-vars "DATABASE_URL=postgresql://postgres:PASSWORD@/tchaas_ledger?host=/cloudsql/tchaas-ledger:us-central1:tchaas-ledger-db" \
    --set-env-vars "GCP_PROJECT_ID=tchaas-ledger" \
    --set-env-vars "ENABLE_GCP_MONITORING=true"
```

## Cloud Monitoring Setup

### View Metrics

```bash
# In Google Cloud Console, navigate to:
# Monitoring > Metrics Explorer

# Or use the command line
gcloud monitoring time-series list \
    --filter='metric.type="prometheus.googleapis.com/http_requests_total/counter"'
```

### Create Alert Policy

```bash
# Create alert for high error rate
gcloud alpha monitoring policies create \
    --notification-channels=CHANNEL_ID \
    --display-name="High Error Rate" \
    --condition-display-name="Error rate > 5%" \
    --condition-threshold-value=0.05 \
    --condition-threshold-duration=60s
```

## IAM Permissions

### Required Roles

For deployment, ensure your account has:
- Cloud Run Admin
- Cloud SQL Admin
- Storage Admin (for container images)
- Monitoring Metric Writer

### Grant Permissions

```bash
# Get your email
gcloud config get-value account

# Grant roles (replace YOUR_EMAIL)
gcloud projects add-iam-policy-binding tchaas-ledger \
    --member="user:YOUR_EMAIL" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding tchaas-ledger \
    --member="user:YOUR_EMAIL" \
    --role="roles/cloudsql.admin"
```

## Service Account Setup

### Create Service Account

```bash
# Create service account for Cloud Run
gcloud iam service-accounts create tchaas-ledger-sa \
    --display-name="Tchaas Ledger Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding tchaas-ledger \
    --member="serviceAccount:tchaas-ledger-sa@tchaas-ledger.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding tchaas-ledger \
    --member="serviceAccount:tchaas-ledger-sa@tchaas-ledger.iam.gserviceaccount.com" \
    --role="roles/monitoring.metricWriter"
```

## Cost Estimation

### Free Tier Eligible Resources

- **Cloud Run**: 2 million requests/month free
- **Cloud SQL**: db-f1-micro with 10GB storage (~$10/month)
- **Cloud Monitoring**: First 150 MiB of logs free
- **Cloud Storage**: 5GB free

### Estimated Monthly Cost

- Development: **~$0** (using free tier)
- Production (low traffic): **~$10-20/month**
- Production (high traffic): **~$50-100/month**

## Testing the Setup

### Local Testing

```bash
cd ~/tchaas-ledger-990/backend

# Activate virtual environment
source venv/bin/activate

# Run the app
python run.py

# Test endpoints
curl http://localhost:5000/health
curl http://localhost:5000/metrics
```

### Production Testing

```bash
# Get Cloud Run URL
gcloud run services describe tchaas-ledger-api \
    --region us-central1 \
    --format='value(status.url)'

# Test health endpoint
curl $(gcloud run services describe tchaas-ledger-api --region us-central1 --format='value(status.url)')/health
```

## Troubleshooting

### Connection Issues

```bash
# Test Cloud SQL connection
gcloud sql connect tchaas-ledger-db --user=postgres

# Check Cloud Run logs
gcloud run logs read tchaas-ledger-api --region us-central1
```

### Monitoring Issues

```bash
# Check if metrics are being sent
gcloud monitoring time-series list \
    --filter='metric.type="custom.googleapis.com/flask/http_requests"' \
    --format=json
```

## Security Best Practices

1. **Never commit credentials** to Git
2. **Use Secret Manager** for sensitive data in production
3. **Enable VPC** for Cloud SQL private IP
4. **Set up Cloud Armor** for DDoS protection
5. **Enable audit logging** for compliance

## Next Steps

1. ✅ Set up local PostgreSQL database
2. ✅ Create database migrations
3. ✅ Test locally
4. ☐ Create Cloud SQL instance
5. ☐ Deploy to Cloud Run
6. ☐ Set up monitoring dashboards
7. ☐ Configure alerts

---

**Last Updated**: 2025-12-09
**Project**: Tchaas Ledger 990
**GCP Project**: tchaas-ledger
