"""
Health Aggregator Service
Provides unified health monitoring across all platform services
"""

from flask import Flask, jsonify, render_template_string
import requests
import time
from datetime import datetime
from collections import defaultdict
import threading

app = Flask(__name__)

# Service registry
SERVICES = {
    "infrastructure": {
        "postgres": {"url": "http://localhost:5532", "check": "tcp"},
        "redis": {"url": "http://localhost:6479", "check": "tcp"},
        "rabbitmq": {"url": "http://localhost:15772", "check": "http"},
        "traefik": {"url": "http://localhost:8181/api/overview", "check": "http"},
    },
    "ai_ml": {
        "ollama": {"url": "http://localhost:11534/api/tags", "check": "http"},
        "weaviate": {"url": "http://localhost:8182/v1/.well-known/ready", "check": "http"},
        "qdrant": {"url": "http://localhost:6333/", "check": "http"},
        "neo4j": {"url": "http://localhost:7474", "check": "http"},
        "elasticsearch": {"url": "http://localhost:9200/_cluster/health", "check": "http"},
        "minio": {"url": "http://localhost:9100/minio/health/live", "check": "http"},
    },
    "backend": {
        "finance": {"url": "http://localhost:8100/health/detailed", "check": "http"},
        "realestate": {"url": "http://localhost:8101/health/detailed", "check": "http"},
        "bondai": {"url": "http://localhost:8102/health", "check": "http"},
        "bondai-agents": {"url": "http://localhost:8105/health/detailed", "check": "http"},
        "legacy": {"url": "http://localhost:8103/health/detailed", "check": "http"},
        "labor": {"url": "http://localhost:8104/health/detailed", "check": "http"},
    },
    "frontend": {
        "unified-dashboard": {"url": "http://localhost:3100", "check": "http"},
        "finance-ui": {"url": "http://localhost:3102", "check": "http"},
        "realestate-ui": {"url": "http://localhost:3103", "check": "http"},
        "bondai-ui": {"url": "http://localhost:3104", "check": "http"},
        "labor-ui": {"url": "http://localhost:3105", "check": "http"},
    },
    "monitoring": {
        "prometheus": {"url": "http://localhost:9190/-/healthy", "check": "http"},
        "grafana": {"url": "http://localhost:3101/api/health", "check": "http"},
        "keycloak": {"url": "http://localhost:8183", "check": "http"},
    }
}

# Health history for metrics
health_history = defaultdict(list)
performance_metrics = defaultdict(list)


def check_health(service_name, service_config):
    """Check health of a single service"""
    start_time = time.time()
    result = {
        "name": service_name,
        "status": "unknown",
        "response_time": None,
        "details": None,
        "timestamp": datetime.now().isoformat()
    }

    try:
        response = requests.get(service_config["url"], timeout=3)
        response_time = (time.time() - start_time) * 1000  # ms

        result["response_time"] = round(response_time, 2)

        if response.status_code == 200:
            result["status"] = "healthy"
            try:
                result["details"] = response.json()
            except:
                result["details"] = {"message": "Service responding"}
        else:
            result["status"] = "degraded"
            result["details"] = {"error": f"HTTP {response.status_code}"}

    except requests.exceptions.Timeout:
        result["status"] = "timeout"
        result["details"] = {"error": "Request timeout"}
    except requests.exceptions.ConnectionError:
        result["status"] = "down"
        result["details"] = {"error": "Connection refused"}
    except Exception as e:
        result["status"] = "error"
        result["details"] = {"error": str(e)}

    # Store metrics
    performance_metrics[service_name].append({
        "response_time": result["response_time"],
        "timestamp": result["timestamp"]
    })

    # Keep only last 100 measurements
    if len(performance_metrics[service_name]) > 100:
        performance_metrics[service_name] = performance_metrics[service_name][-100:]

    return result


def check_all_services():
    """Check health of all services"""
    results = {}
    for category, services in SERVICES.items():
        results[category] = {}
        for service_name, service_config in services.items():
            results[category][service_name] = check_health(service_name, service_config)

    return results


def calculate_health_score(results):
    """Calculate overall platform health score"""
    total = 0
    healthy = 0

    for category, services in results.items():
        for service_name, status in services.items():
            total += 1
            if status["status"] == "healthy":
                healthy += 1

    return round((healthy / total * 100), 2) if total > 0 else 0


@app.route("/")
def index():
    """Health dashboard HTML"""
    return render_template_string(DASHBOARD_HTML)


@app.route("/api/health")
def health():
    """Aggregated health check endpoint"""
    results = check_all_services()
    health_score = calculate_health_score(results)

    # Count by status
    status_counts = {"healthy": 0, "degraded": 0, "down": 0, "timeout": 0, "error": 0, "unknown": 0}
    for category, services in results.items():
        for service_name, status in services.items():
            status_counts[status["status"]] = status_counts.get(status["status"], 0) + 1

    return jsonify({
        "overall_status": "healthy" if health_score >= 90 else "degraded" if health_score >= 70 else "critical",
        "health_score": health_score,
        "status_counts": status_counts,
        "services": results,
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/metrics")
def metrics():
    """Performance metrics endpoint"""
    metrics_summary = {}

    for service_name, measurements in performance_metrics.items():
        if measurements:
            response_times = [m["response_time"] for m in measurements if m["response_time"] is not None]
            if response_times:
                metrics_summary[service_name] = {
                    "avg_response_time": round(sum(response_times) / len(response_times), 2),
                    "min_response_time": round(min(response_times), 2),
                    "max_response_time": round(max(response_times), 2),
                    "sample_count": len(response_times)
                }

    return jsonify(metrics_summary)


@app.route("/api/prometheus")
def prometheus_metrics():
    """Export metrics in Prometheus format"""
    results = check_all_services()
    metrics = []

    # Service status (1 = healthy, 0 = unhealthy)
    for category, services in results.items():
        for service_name, status in services.items():
            value = 1 if status["status"] == "healthy" else 0
            metrics.append(f'service_health{{service="{service_name}",category="{category}"}} {value}')

            # Response time
            if status["response_time"] is not None:
                metrics.append(f'service_response_time_ms{{service="{service_name}",category="{category}"}} {status["response_time"]}')

    # Overall health score
    health_score = calculate_health_score(results)
    metrics.append(f'platform_health_score {health_score}')

    return "\n".join(metrics), 200, {"Content-Type": "text/plain"}


# HTML Dashboard Template
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Platform Health Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 {
            font-size: 2rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle { color: #94a3b8; margin-bottom: 30px; }
        .score-card {
            background: #1e293b;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            border: 1px solid #334155;
        }
        .score {
            font-size: 4rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
        .score.healthy { color: #10b981; }
        .score.degraded { color: #f59e0b; }
        .score.critical { color: #ef4444; }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .status-item {
            background: #334155;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .status-count {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .category {
            background: #1e293b;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #334155;
        }
        .category h2 {
            font-size: 1.5rem;
            margin-bottom: 15px;
            color: #a78bfa;
        }
        .service-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }
        .service-card {
            background: #334155;
            border-radius: 8px;
            padding: 15px;
            border-left: 4px solid #64748b;
        }
        .service-card.healthy { border-left-color: #10b981; }
        .service-card.degraded { border-left-color: #f59e0b; }
        .service-card.down { border-left-color: #ef4444; }
        .service-card.timeout { border-left-color: #f97316; }
        .service-name {
            font-weight: 600;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .status-badge {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        .status-badge.healthy { background: #10b981; color: white; }
        .status-badge.degraded { background: #f59e0b; color: white; }
        .status-badge.down { background: #ef4444; color: white; }
        .status-badge.timeout { background: #f97316; color: white; }
        .status-badge.error { background: #dc2626; color: white; }
        .response-time {
            color: #94a3b8;
            font-size: 0.875rem;
            margin-top: 5px;
        }
        .refresh-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #334155;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 0.875rem;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .loading { animation: pulse 2s ease-in-out infinite; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 Platform Health Dashboard</h1>
        <p class="subtitle">Real-time monitoring of all platform services</p>

        <div class="refresh-indicator" id="refreshIndicator">
            Auto-refresh: <span id="countdown">10</span>s
        </div>

        <div id="dashboard">Loading...</div>
    </div>

    <script>
        let countdown = 10;

        async function fetchHealth() {
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                renderDashboard(data);
            } catch (error) {
                console.error('Error fetching health:', error);
            }
        }

        function renderDashboard(data) {
            const statusClass = data.overall_status;
            const html = `
                <div class="score-card">
                    <div class="score ${statusClass}">${data.health_score}%</div>
                    <div style="text-align: center; color: #94a3b8; font-size: 1.125rem;">
                        Platform Health Score
                    </div>
                    <div class="status-grid">
                        <div class="status-item">
                            <div class="status-count" style="color: #10b981">${data.status_counts.healthy || 0}</div>
                            <div style="color: #94a3b8; font-size: 0.875rem">Healthy</div>
                        </div>
                        <div class="status-item">
                            <div class="status-count" style="color: #f59e0b">${data.status_counts.degraded || 0}</div>
                            <div style="color: #94a3b8; font-size: 0.875rem">Degraded</div>
                        </div>
                        <div class="status-item">
                            <div class="status-count" style="color: #ef4444">${data.status_counts.down || 0}</div>
                            <div style="color: #94a3b8; font-size: 0.875rem">Down</div>
                        </div>
                        <div class="status-item">
                            <div class="status-count" style="color: #f97316">${data.status_counts.timeout || 0}</div>
                            <div style="color: #94a3b8; font-size: 0.875rem">Timeout</div>
                        </div>
                    </div>
                </div>

                ${Object.entries(data.services).map(([category, services]) => `
                    <div class="category">
                        <h2>${category.replace('_', ' ').toUpperCase()}</h2>
                        <div class="service-grid">
                            ${Object.entries(services).map(([name, status]) => `
                                <div class="service-card ${status.status}">
                                    <div class="service-name">
                                        <span>${name}</span>
                                        <span class="status-badge ${status.status}">${status.status}</span>
                                    </div>
                                    ${status.response_time !== null ? `
                                        <div class="response-time">⚡ ${status.response_time}ms</div>
                                    ` : ''}
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `).join('')}
            `;

            document.getElementById('dashboard').innerHTML = html;
        }

        // Auto-refresh
        setInterval(() => {
            countdown--;
            document.getElementById('countdown').textContent = countdown;

            if (countdown <= 0) {
                fetchHealth();
                countdown = 10;
            }
        }, 1000);

        // Initial load
        fetchHealth();
    </script>
</body>
</html>
'''

if __name__ == "__main__":
    print("🏥 Starting Health Aggregator Service")
    print("📊 Dashboard: http://localhost:8200")
    print("🔌 API: http://localhost:8200/api/health")
    print("📈 Metrics: http://localhost:8200/api/prometheus")
    app.run(host="0.0.0.0", port=8200, debug=False)
