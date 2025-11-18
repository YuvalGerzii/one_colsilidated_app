# Market Intelligence Daily Update - Scheduling Guide

## Overview

The market intelligence update system automatically fetches and stores:
- Stock market data (REITs, indices, rates) from YFinance
- Economic indicators (GDP, employment, housing) from Economics API
- Daily comprehensive market snapshots

## Recommended Schedule

**Primary Update**: Daily at **6:00 PM EST** (after US market close)

### Why 6 PM EST?
- US stock markets close at 4:00 PM EST
- Gives 2 hours for data to settle and be processed
- Economic data releases are typically complete by this time
- Avoids market hours volatility

## Setup Methods

### Method 1: Cron (Linux/Mac) - Recommended for Servers

#### Quick Setup

```bash
# 1. Create log directory
sudo mkdir -p /var/log/market_intelligence
sudo chown $USER:$USER /var/log/market_intelligence

# 2. Test the script
cd /home/user/real_estate_dashboard/backend
python3 scripts/update_market_intelligence.py

# 3. Add to crontab
crontab -e

# 4. Add this line (adjust path as needed):
0 18 * * * cd /home/user/real_estate_dashboard/backend && /usr/local/bin/python3 scripts/update_market_intelligence.py >> /var/log/market_intelligence/daily_update.log 2>&1
```

#### Advanced Cron Configuration

```bash
# Run with retry mechanism
0 18 * * * cd /path/to/backend && python3 scripts/update_market_intelligence.py || python3 scripts/update_market_intelligence.py --force

# Run on weekdays only (Mon-Fri)
0 18 * * 1-5 cd /path/to/backend && python3 scripts/update_market_intelligence.py

# Run with email notification on failure (requires mailx)
0 18 * * * cd /path/to/backend && python3 scripts/update_market_intelligence.py || echo "Update failed" | mail -s "Market Update Alert" admin@domain.com
```

See `scripts/crontab.example` for more configurations.

### Method 2: Systemd Timer (Linux) - Recommended for Production

#### Installation

```bash
# 1. Copy service files
sudo cp backend/scripts/systemd/market-intelligence-update.service /etc/systemd/system/
sudo cp backend/scripts/systemd/market-intelligence-update.timer /etc/systemd/system/

# 2. Reload systemd
sudo systemctl daemon-reload

# 3. Enable timer (starts on boot)
sudo systemctl enable market-intelligence-update.timer

# 4. Start timer now
sudo systemctl start market-intelligence-update.timer

# 5. Check status
sudo systemctl status market-intelligence-update.timer
sudo systemctl list-timers
```

#### Systemd Management

```bash
# Check timer status
sudo systemctl status market-intelligence-update.timer

# View logs
sudo journalctl -u market-intelligence-update.service -f

# Run manually
sudo systemctl start market-intelligence-update.service

# Stop timer
sudo systemctl stop market-intelligence-update.timer

# Disable timer
sudo systemctl disable market-intelligence-update.timer
```

#### Customize Schedule

Edit `/etc/systemd/system/market-intelligence-update.timer`:

```ini
# Daily at 6 PM
OnCalendar=*-*-* 18:00:00

# Twice daily (6 AM and 6 PM)
OnCalendar=*-*-* 06:00:00
OnCalendar=*-*-* 18:00:00

# Weekdays only at 6 PM
OnCalendar=Mon..Fri *-*-* 18:00:00

# Every 6 hours
OnCalendar=*-*-* 00,06,12,18:00:00
```

After editing, reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart market-intelligence-update.timer
```

### Method 3: Python Scheduler (Cross-platform)

For development or Windows environments:

```python
# backend/app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.market_intelligence_updater import run_daily_update

scheduler = AsyncIOScheduler()

# Run daily at 6 PM
scheduler.add_job(
    run_daily_update,
    'cron',
    hour=18,
    minute=0,
    id='market_intelligence_update'
)

scheduler.start()
```

Add to `main.py` startup:
```python
from app.scheduler import scheduler

@app.on_event("startup")
async def start_scheduler():
    scheduler.start()
```

### Method 4: Docker Container (Cloud Deployment)

```dockerfile
# Dockerfile.updater
FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

CMD ["python3", "scripts/update_market_intelligence.py"]
```

```yaml
# docker-compose.yml
services:
  market-intelligence-updater:
    build:
      context: .
      dockerfile: Dockerfile.updater
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    restart: unless-stopped
    # Run daily at 6 PM using cron
    command: >
      sh -c "echo '0 18 * * * python3 /app/scripts/update_market_intelligence.py' | crontab - && crond -f"
```

### Method 5: AWS Lambda (Serverless)

```yaml
# serverless.yml
functions:
  marketIntelligenceUpdate:
    handler: scripts/update_market_intelligence.lambda_handler
    timeout: 900  # 15 minutes
    events:
      - schedule:
          rate: cron(0 18 * * ? *)  # 6 PM daily
          description: Daily market intelligence update
```

## Manual Execution

### Run Update Now

```bash
cd /home/user/real_estate_dashboard/backend
python3 scripts/update_market_intelligence.py
```

### Dry Run (Test without saving)

```bash
python3 scripts/update_market_intelligence.py --dry-run
```

### Force Update (Ignore recent update checks)

```bash
python3 scripts/update_market_intelligence.py --force
```

### Verbose Output

```bash
python3 scripts/update_market_intelligence.py --verbose
```

## Monitoring & Logs

### View Logs

```bash
# Cron logs
tail -f /var/log/market_intelligence/daily_update.log

# Systemd logs
sudo journalctl -u market-intelligence-update.service -f

# Python logging
tail -f /home/user/real_estate_dashboard/backend/logs/market_intelligence.log
```

### Log Rotation

Create `/etc/logrotate.d/market-intelligence`:

```
/var/log/market_intelligence/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 $USER $USER
    sharedscripts
    postrotate
        # Optional: restart service if needed
    endscript
}
```

## Notification Setup

### Email Notifications on Failure

```bash
# Install mailx
sudo apt-get install mailutils  # Ubuntu/Debian
sudo yum install mailx          # CentOS/RHEL

# Add to cron
0 18 * * * cd /path/to/backend && python3 scripts/update_market_intelligence.py || echo "Update failed: $(date)" | mail -s "Market Intelligence Alert" admin@domain.com
```

### Slack Notifications

Add to `market_intelligence_updater.py`:

```python
import requests

def send_slack_notification(message, webhook_url):
    requests.post(webhook_url, json={"text": message})

# In run_daily_update():
if self.status['total_failures'] > 0:
    send_slack_notification(
        f"⚠️ Market Intelligence Update had {self.status['total_failures']} failures",
        os.getenv("SLACK_WEBHOOK_URL")
    )
```

### Discord Notifications

```python
def send_discord_notification(message, webhook_url):
    requests.post(webhook_url, json={"content": message})
```

## Fallback Mechanisms

The update script includes automatic fallbacks:

1. **Retry Logic**: 3 attempts with exponential backoff
2. **Cache Fallback**: Uses cached data if API fails (up to 24 hours)
3. **Database Fallback**: Uses yesterday's data if cache unavailable
4. **Graceful Degradation**: Continues with available data sources

## Troubleshooting

### Update Not Running

```bash
# Check cron service
sudo systemctl status cron

# Check cron logs
grep CRON /var/log/syslog

# Check script permissions
ls -la scripts/update_market_intelligence.py

# Test script manually
python3 scripts/update_market_intelligence.py --verbose
```

### Database Connection Issues

```bash
# Check database connectivity
psql -h localhost -U postgres -d real_estate_dashboard

# Check environment variables
echo $DATABASE_URL
```

### API Rate Limiting

If hitting rate limits:
- Reduce update frequency
- Add longer delays between API calls
- Use caching more aggressively

## Performance Optimization

### Optimize Update Time

```python
# Run updates in parallel
async def run_parallel_updates():
    tasks = [
        update_yfinance_data(),
        update_economics_data(),
    ]
    await asyncio.gather(*tasks)
```

### Reduce Database Load

- Batch insert records
- Use upsert instead of select-then-update
- Index frequently queried columns

## Security Considerations

1. **API Keys**: Store in environment variables, never commit
2. **Database Access**: Use read-only user for queries
3. **Log Sanitization**: Remove sensitive data from logs
4. **Rate Limiting**: Respect API rate limits

## Best Practices

✅ **DO:**
- Run after market close (6 PM EST)
- Monitor logs regularly
- Test updates manually before scheduling
- Keep update script under 30 minutes execution
- Use caching to reduce API calls

❌ **DON'T:**
- Run during market hours (causes stale data)
- Run more than once per hour (API rate limits)
- Ignore failed updates
- Hard-code API keys
- Skip error handling

## Support

For issues or questions:
1. Check logs first
2. Test manual execution
3. Review API status pages:
   - YFinance: Check Yahoo Finance status
   - Economics API: https://economics-api.apidog.io/health

## Summary

**Recommended Setup:**
- Use systemd timer for production Linux servers
- Use cron for simple setups or shared hosting
- Run daily at 6 PM EST
- Monitor logs for failures
- Set up notifications for critical failures

**Quick Start:**
```bash
# 1. Test manually
python3 scripts/update_market_intelligence.py

# 2. Add to cron
crontab -e
0 18 * * * cd /home/user/real_estate_dashboard/backend && python3 scripts/update_market_intelligence.py

# 3. Monitor
tail -f /var/log/market_intelligence/daily_update.log
```
