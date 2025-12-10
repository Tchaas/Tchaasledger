# 💰 Hosting Cost Analysis - Tchaas Ledger 990

**Last Updated**: 2025-12-09
**Currency**: USD
**Region**: us-central1 (Iowa)

## 📊 Monthly Cost Breakdown

### 🟢 Development/Testing (Low Traffic)
**Estimated Monthly Cost**: **$0-15/month**

| Service | Usage | Cost |
|---------|-------|------|
| Cloud Run (Backend API) | 2M requests, 360k vCPU-seconds | **FREE** (within free tier) |
| Cloud Storage (Static Frontend) | 5GB storage, minimal egress | **FREE** (within free tier) |
| Cloud SQL (PostgreSQL) | db-f1-micro, 10GB SSD | **~$8-10/month** |
| Cloud Monitoring | 150 MiB logs, basic metrics | **FREE** (within free tier) |
| Cloud Build | 120 builds/month | **FREE** (within free tier) |
| **TOTAL** | | **$8-10/month** |

### 🟡 Production (Low-Medium Traffic)
**Estimated Monthly Cost**: **$25-50/month**

| Service | Usage | Cost |
|---------|-------|------|
| Cloud Run (Backend API) | 5M requests, 1M vCPU-seconds, 500 GB-hours | **~$10-15/month** |
| Cloud Storage (Static Frontend) | 10GB storage, 50GB egress | **~$2-3/month** |
| Cloud SQL (PostgreSQL) | db-g1-small, 20GB SSD, backups | **~$35-40/month** |
| Cloud Monitoring | 500 MiB logs, custom metrics | **~$2-3/month** |
| Load Balancer (Optional) | Minimal traffic | **~$5/month** |
| **TOTAL** | | **$54-66/month** |

### 🔴 Production (High Traffic)
**Estimated Monthly Cost**: **$150-300/month**

| Service | Usage | Cost |
|---------|-------|------|
| Cloud Run (Backend API) | 20M requests, 5M vCPU-seconds, 2000 GB-hours | **~$50-75/month** |
| Cloud Storage (Frontend) | 50GB storage, 500GB egress | **~$15-20/month** |
| Cloud SQL (PostgreSQL) | db-n1-standard-1, 100GB SSD, HA, backups | **~$120-150/month** |
| Cloud Monitoring | 2GB logs, extensive metrics | **~$10-15/month** |
| Load Balancer | High traffic | **~$20-25/month** |
| Cloud CDN (Optional) | Caching, 1TB egress | **~$20-30/month** |
| **TOTAL** | | **$235-315/month** |

## 📈 Cost by User Scale

### Personal/Side Project (You Only)
- **Users**: Just you testing
- **Monthly Cost**: **$0-8/month**
- **Configuration**: Development setup, no Cloud SQL (use local PostgreSQL)
- **What's Free**:
  - Cloud Run (2M requests/month)
  - Cloud Storage (5GB)
  - Cloud Monitoring (150 MiB logs)

### Small Nonprofit (1-10 users)
- **Users**: 1-10 concurrent users
- **Requests**: ~100k-500k/month
- **Monthly Cost**: **$8-15/month**
- **Configuration**:
  - Cloud Run: Auto-scale 0-2 instances
  - Cloud SQL: db-f1-micro
  - Basic monitoring

### Medium Nonprofit (10-100 users)
- **Users**: 10-100 concurrent users
- **Requests**: ~1M-5M/month
- **Monthly Cost**: **$50-100/month**
- **Configuration**:
  - Cloud Run: Auto-scale 0-5 instances
  - Cloud SQL: db-g1-small with backups
  - Enhanced monitoring

### Large Organization (100+ users)
- **Users**: 100-1000+ concurrent users
- **Requests**: ~10M-50M/month
- **Monthly Cost**: **$200-500/month**
- **Configuration**:
  - Cloud Run: Auto-scale 0-20 instances
  - Cloud SQL: db-n1-standard-2, High Availability
  - Full monitoring stack
  - CDN for global distribution

## 🆓 Free Tier Details (Google Cloud)

### Always Free (No time limit)
- **Cloud Run**:
  - 2 million requests/month
  - 360,000 vCPU-seconds/month
  - 180,000 GiB-seconds/month
- **Cloud Storage**:
  - 5 GB storage/month
  - 5,000 Class A operations/month
  - 50,000 Class B operations/month
  - 1 GB network egress/month
- **Cloud Monitoring**:
  - First 150 MiB of logs/month
  - Basic metrics

### NOT Free (Main Costs)
- **Cloud SQL**: No free tier - starts at ~$8/month for db-f1-micro
- **Networking**: Egress over 1GB/month
- **Cloud Build**: Over 120 builds/month
- **Persistent Disks**: Storage beyond free tier

## 💡 Cost Optimization Strategies

### 1. Start Minimal (Recommended)
**Cost**: $8-15/month
```yaml
Strategy:
  - Use Cloud Run serverless (scales to zero)
  - Smallest Cloud SQL instance (db-f1-micro)
  - No load balancer initially
  - Basic monitoring only
  - Single region deployment
```

### 2. Use Local Database for Development
**Cost**: $0/month (development only)
```yaml
Strategy:
  - Deploy backend to Cloud Run (free tier)
  - Use local PostgreSQL database
  - No Cloud SQL charges
  - Perfect for testing and demos
```

### 3. Deploy Frontend Only
**Cost**: $0/month
```yaml
Strategy:
  - Deploy React app to Cloud Storage
  - Use Firebase Hosting (free tier)
  - Mock data or external API
  - No backend costs
```

### 4. Scheduled Shutdown (For Development)
**Cost**: ~$2-5/month
```yaml
Strategy:
  - Auto-shutdown Cloud SQL at night
  - Use Cloud Scheduler to start/stop
  - ~12 hours/day = 50% cost savings
  - Perfect for development environments
```

## 📊 Traffic-Based Cost Calculator

### Cost Per 1,000 Requests
- **Cloud Run**: $0.00 (within free tier) to $0.40 (at scale)
- **Cloud SQL**: $0.00 (fixed cost, not per request)
- **Total Per 1k Requests**: $0.00-0.40

### Example Scenarios

**Scenario 1: Personal Use (1,000 requests/month)**
- Cloud Run: FREE
- Cloud SQL: $8/month
- **Total**: $8/month

**Scenario 2: Small Nonprofit (100,000 requests/month)**
- Cloud Run: FREE (within 2M free tier)
- Cloud SQL: $8-10/month
- **Total**: $8-10/month

**Scenario 3: Growing Org (1,000,000 requests/month)**
- Cloud Run: FREE (within 2M free tier)
- Cloud SQL: $35-40/month (need larger instance)
- **Total**: $35-40/month

**Scenario 4: Popular Service (10,000,000 requests/month)**
- Cloud Run: $40-50/month (beyond free tier)
- Cloud SQL: $120-150/month (need HA setup)
- **Total**: $160-200/month

## 🔍 Detailed Component Costs

### Cloud Run (Backend API)
```
Pricing:
- CPU: $0.00002400 per vCPU-second
- Memory: $0.00000250 per GiB-second
- Requests: $0.40 per million requests
- Container instance time: Billed when serving requests

Free Tier (Monthly):
- 2 million requests
- 360,000 vCPU-seconds
- 180,000 GiB-seconds
- First 180,000 GiB-seconds free
```

**Your estimated usage**:
- Small: FREE (within limits)
- Medium: $10-15/month (500GB-hours, 5M requests)
- Large: $50-75/month (2000GB-hours, 20M requests)

### Cloud SQL (PostgreSQL Database)
```
Pricing (us-central1):
- db-f1-micro: $7.67/month (shared CPU, 0.6GB RAM, 3GB storage)
- db-g1-small: $25.00/month (shared CPU, 1.7GB RAM, 10GB storage)
- db-n1-standard-1: $46.38/month (1 vCPU, 3.75GB RAM)
- db-n1-standard-2: $92.76/month (2 vCPU, 7.5GB RAM)

Additional:
- SSD storage: $0.17/GB/month
- Backups: $0.08/GB/month
- High Availability: 2x instance cost
- Network egress: $0.12/GB
```

**Recommended tiers**:
- Development: db-f1-micro ($8/month)
- Small nonprofit: db-g1-small ($25-35/month with storage)
- Medium nonprofit: db-n1-standard-1 ($50-70/month with HA)
- Large org: db-n1-standard-2 HA ($200-250/month)

### Cloud Storage (Frontend Hosting)
```
Pricing:
- Storage: $0.020/GB/month
- Class A operations: $0.05 per 10,000
- Class B operations: $0.004 per 10,000
- Network egress: $0.12/GB (after first 1GB free)

Free Tier:
- 5 GB storage
- 5,000 Class A operations
- 50,000 Class B operations
- 1 GB egress
```

**Your estimated cost**:
- Small: FREE (within limits)
- Medium: $2-5/month (10GB storage, 50GB egress)
- Large: $15-30/month (50GB storage, 500GB egress)

### Cloud Monitoring & Logging
```
Pricing:
- Log ingestion: $0.50/GB
- Log storage: $0.01/GB/month
- Metrics: $0.2580/MiB
- Traces: $0.20/million spans

Free Tier:
- First 50 GiB logs/month
- First 150 MiB of metrics/month
```

**Your estimated cost**:
- Small: FREE
- Medium: $2-5/month
- Large: $10-20/month

## 🌐 Alternative Hosting Options

### Option 1: Google Cloud (Recommended)
**Pros**: Excellent integration, auto-scaling, monitoring
**Cons**: Minimum cost ~$8/month for database
**Best For**: Production use, scaling, monitoring

### Option 2: Railway.app
**Cost**: $5/month minimum
**Pros**: Simple deployment, PostgreSQL included, good for startups
**Cons**: Limited free tier, less control
**Best For**: Quick MVP, small projects

### Option 3: Render.com
**Cost**: $0-25/month
**Pros**: Free PostgreSQL (90 days), easy deployment
**Cons**: Free DB expires, slower cold starts
**Best For**: Prototypes, demos

### Option 4: Fly.io
**Cost**: $0-10/month
**Pros**: Generous free tier, PostgreSQL included
**Cons**: Learning curve, community support
**Best For**: Side projects, development

### Option 5: Heroku
**Cost**: $7-25/month
**Pros**: Simple, well-documented
**Cons**: More expensive, slower performance
**Best For**: Quick deployment, low traffic

### Option 6: DigitalOcean App Platform
**Cost**: $12-25/month
**Pros**: Predictable pricing, managed database
**Cons**: Less auto-scaling
**Best For**: Steady traffic, budget-conscious

## 💰 Recommended Configuration by Budget

### Budget: $0/month (Testing Only)
```yaml
Configuration:
  - Frontend: GitHub Pages or Vercel (free)
  - Backend: Cloud Run (free tier)
  - Database: Local PostgreSQL or Supabase (free tier)
  - Monitoring: Basic only
Limitations:
  - No persistent database in cloud
  - Manual restarts needed
  - Limited monitoring
```

### Budget: $10/month (Personal/Small Nonprofit)
```yaml
Configuration:
  - Frontend: Cloud Storage or Firebase Hosting
  - Backend: Cloud Run (free tier likely sufficient)
  - Database: Cloud SQL db-f1-micro ($8/month)
  - Monitoring: Free tier
Users Supported: 1-10 concurrent
Traffic: ~500k requests/month
```

### Budget: $50/month (Growing Nonprofit)
```yaml
Configuration:
  - Frontend: Cloud Storage with CDN
  - Backend: Cloud Run (auto-scale 0-5)
  - Database: Cloud SQL db-g1-small with backups ($35/month)
  - Monitoring: Enhanced ($5/month)
  - Load Balancer: Optional ($5/month)
Users Supported: 10-50 concurrent
Traffic: ~2M requests/month
```

### Budget: $100/month (Established Organization)
```yaml
Configuration:
  - Frontend: Cloud Storage + Cloud CDN
  - Backend: Cloud Run (auto-scale 0-10)
  - Database: Cloud SQL db-n1-standard-1 with HA ($70/month)
  - Monitoring: Full stack ($10/month)
  - Load Balancer: Yes ($7/month)
  - Backups: Automated daily
Users Supported: 50-200 concurrent
Traffic: ~5M requests/month
```

## 📅 Annual Cost Projection

### Conservative Estimate (Start Small, Grow Gradually)
| Month | Users | Monthly Cost | Annual Total |
|-------|-------|--------------|--------------|
| 1-3   | 1-5   | $10/month    | $30          |
| 4-6   | 5-15  | $15/month    | $45          |
| 7-9   | 15-30 | $35/month    | $105         |
| 10-12 | 30-50 | $50/month    | $150         |
| **Year 1 Total** | | | **$330/year** |

### Aggressive Growth Estimate
| Month | Users | Monthly Cost | Annual Total |
|-------|-------|--------------|--------------|
| 1-3   | 10-30 | $50/month    | $150         |
| 4-6   | 30-100| $100/month   | $300         |
| 7-9   | 100-300| $200/month  | $600         |
| 10-12 | 300-500| $300/month  | $900         |
| **Year 1 Total** | | | **$1,950/year** |

## 🎯 My Recommendation for Tchaas Ledger

### Phase 1: Launch (Months 1-3)
**Budget**: $10-15/month
```yaml
Setup:
  - Cloud Run (free tier)
  - Cloud SQL db-f1-micro ($8/month)
  - Basic monitoring
Goal: Get product launched, gather feedback
Users: 1-10 users testing
```

### Phase 2: Growth (Months 4-6)
**Budget**: $35-50/month
```yaml
Setup:
  - Cloud Run (still likely free)
  - Cloud SQL db-g1-small ($35/month)
  - Enhanced monitoring
Goal: Onboard first real nonprofits
Users: 10-30 active users
```

### Phase 3: Scale (Months 7-12)
**Budget**: $75-150/month
```yaml
Setup:
  - Cloud Run (auto-scale)
  - Cloud SQL db-n1-standard-1 ($70/month)
  - Full monitoring + alerts
  - CDN enabled
Goal: Serve multiple organizations
Users: 50-100+ active users
```

## 💡 Key Takeaways

1. **Start Minimal**: Begin with $8-10/month (db-f1-micro)
2. **Leverage Free Tiers**: Cloud Run is free for most startups
3. **Database is Main Cost**: 60-80% of your bill
4. **Scale Gradually**: Only upgrade when needed
5. **Monitor Usage**: Set up billing alerts early
6. **Use Auto-Scaling**: Pay only for what you use

## 🚨 Cost Alerts Setup

Set up billing alerts at:
- **$10**: First warning (basic costs)
- **$25**: Moderate warning (growing)
- **$50**: High warning (review needed)
- **$100**: Critical (immediate review)

```bash
# Set up billing alert via gcloud
gcloud alpha billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="Tchaas Ledger Budget" \
  --budget-amount=50 \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90
```

## 📞 Questions to Ask Yourself

1. **How many users will I have in month 1?**
   - 1-10: $10/month
   - 10-50: $35/month
   - 50+: $75+/month

2. **How often will users access the system?**
   - Daily: Plan for higher Cloud Run costs
   - Weekly: Free tier likely sufficient
   - Monthly: Definitely free tier

3. **Do I need high availability?**
   - Yes: Add 100% to database cost
   - No: Use single instance

4. **What's my data retention policy?**
   - Forever: Plan for storage growth
   - 1 year: Moderate storage costs
   - Archive old data: Lower costs

## 🎁 Special Offers & Credits

- **Google Cloud Free Trial**: $300 credit for 90 days
- **Startups**: Google for Startups (up to $100k credits)
- **Nonprofits**: Google for Nonprofits (discounts available)
- **Students**: GitHub Student Developer Pack (various credits)

---

**Bottom Line**: For Tchaas Ledger 990, expect to spend:
- **Development/Testing**: $0-10/month
- **Launch (1-10 users)**: $10-15/month
- **Growing (10-50 users)**: $35-75/month
- **Established (50-200 users)**: $75-150/month
- **Large Scale (200+ users)**: $150-300/month

**Start with the $10/month plan and scale as you grow!** 🚀
