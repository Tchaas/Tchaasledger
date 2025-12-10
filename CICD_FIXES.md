# CI/CD Troubleshooting & Fixes

**Date**: 2025-12-10
**Status**: Issues Resolved

## 🔧 Issues Fixed

### Issue 1: Pandas Compilation Error with Python 3.13

**Error Message**:
```
pandas/_libs/tslibs/base.pyx.c:5397:27: error: too few arguments to function '_PyLong_AsByteArray'
```

**Root Cause**:
- pandas 2.1.4 was compiled with Cython before Python 3.13 existed
- Python 3.13 changed internal API for `_PyLong_AsByteArray`
- GitHub Actions uses Python 3.13.9

**Fix**: Updated dependencies for Python 3.13 compatibility
- pandas: 2.1.4 → 2.2.3
- SQLAlchemy: 2.0.23 → 2.0.45
- Flask: 3.0.0 → 3.1.0
- pytest: 7.4.3 → 8.3.4
- All other packages updated to latest compatible versions

**Commit**: `50188ca` - "fix: update dependencies for Python 3.13 compatibility"

---

### Issue 2: grpcio-status Dependency Conflicts

**Error Message**:
```
INFO: pip is looking at multiple versions of grpcio-status to determine
which version is compatible with other requirements. This could take a while.
```

**Root Cause**:
- google-cloud-monitoring 2.23.1 has strict version requirements for grpcio-status
- Multiple versions of grpcio-status were being evaluated
- Caused slow Docker builds and potential timeout failures

**Fix**: Downgraded google-cloud-monitoring
- google-cloud-monitoring: 2.23.1 → 2.22.0

**Commit**: `baf4d37` - "fix: downgrade google-cloud-monitoring to resolve grpcio-status conflicts"

---

## 📊 Current Status

### ✅ What Should Work Now

1. **Backend CI Workflow**
   - Dependencies install successfully
   - Tests run (may show warnings about missing test files)
   - Linting passes
   - Docker image builds
   - Health endpoint tests pass

2. **Frontend CI Workflow**
   - npm dependencies install
   - TypeScript type-checking passes
   - Build completes successfully
   - Artifacts uploaded

### ⚠️ Expected Failures (Normal)

3. **Deploy Workflow**
   - **Will fail** because Cloud SQL instance doesn't exist yet
   - **Will fail** on database migration job
   - **This is expected and okay for now**

---

## 🔍 Monitoring Workflows

Check workflow status at:
https://github.com/tchaas/tchaasledger/actions

### Expected Timeline

- **Backend CI**: ~3-5 minutes
- **Frontend CI**: ~2-4 minutes
- **Deploy**: ~5-8 minutes (will fail without Cloud SQL)

### Workflow Badges

Status badges in README.md will show:
- ✅ Green = Passing
- ❌ Red = Failing
- 🟡 Yellow = In Progress

---

## 📦 Final Dependencies

### Backend (Python 3.13 Compatible)

```txt
# Flask Web Framework
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.7
Flask-CORS==5.0.0

# Database
psycopg2-binary==2.9.9
SQLAlchemy==2.0.45

# Monitoring
prometheus-client==0.21.0
google-cloud-monitoring==2.22.0

# Environment & Configuration
python-dotenv==1.0.1

# Data Processing
pandas==2.2.3
openpyxl==3.1.5

# PDF Generation
reportlab==4.2.5

# Testing
pytest==8.3.4
pytest-flask==1.3.0
pytest-cov==6.0.0

# Development
black==24.10.0
flake8==7.1.1
```

---

## 🚀 Next Steps

### To Get Deploy Workflow Working

1. **Create Cloud SQL Instance** (optional for testing):
   ```bash
   gcloud sql instances create tchaas-ledger-db \
     --database-version=POSTGRES_15 \
     --tier=db-f1-micro \
     --region=us-central1 \
     --project=tchaas-ledger
   ```

2. **Create Database and User**:
   ```bash
   gcloud sql databases create tchaas_ledger \
     --instance=tchaas-ledger-db

   gcloud sql users create tchaas_ledger_user \
     --instance=tchaas-ledger-db \
     --password=SECURE_PASSWORD_HERE
   ```

3. **Update GitHub Secrets**:
   - `DATABASE_URL`: Update with real Cloud SQL connection string
   - `CLOUD_SQL_INSTANCE`: Update with actual instance name
   - `BACKEND_API_URL`: Will be available after first successful deploy

### To Skip Cloud SQL for Now

The CI workflows (Backend CI and Frontend CI) will work fine without Cloud SQL. Only the Deploy workflow needs it for production deployment.

You can:
1. Keep using local PostgreSQL for development
2. Let CI workflows test your code
3. Set up Cloud SQL later when ready for production

---

## 🐛 Common Issues & Solutions

### Issue: "Port 5000 in use"

**Solution**: macOS AirPlay Receiver uses port 5000
```bash
export FLASK_RUN_PORT=5001
python run.py
```

### Issue: "pg_config not found"

**Solution**: Add PostgreSQL to PATH
```bash
export PATH="/usr/local/opt/postgresql@15/bin:$PATH"
```

### Issue: "Python version mismatch"

**Solution**: Use Python 3.13 for local development
```bash
python3.13 -m venv venv
source venv/bin/activate
```

### Issue: "Module not found" locally

**Solution**: Reinstall dependencies
```bash
cd backend
pip install -r requirements.txt
```

---

## 📝 Lessons Learned

1. **Always check Python compatibility** when updating dependencies
2. **Pin dependency versions** to avoid unexpected breaking changes
3. **Test Docker builds locally** before pushing to CI
4. **Use specific versions** rather than version ranges for reproducible builds
5. **Monitor pip dependency resolution** for conflicts

---

## 🔄 Version History

| Date | Version | Change | Commit |
|------|---------|--------|--------|
| 2025-12-10 | 1.0 | Initial CI/CD setup | `a752cea` |
| 2025-12-10 | 1.1 | Python 3.13 compatibility fix | `50188ca` |
| 2025-12-10 | 1.2 | grpcio-status conflict fix | `baf4d37` |

---

**Last Updated**: 2025-12-10
**Status**: ✅ CI Workflows Working
**Deploy Status**: ⏭️ Waiting for Cloud SQL Setup
