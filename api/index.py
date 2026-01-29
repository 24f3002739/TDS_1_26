from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import statistics

app = FastAPI()

# Simple CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyticsRequest(BaseModel):
    regions: list[str]
    threshold_ms: float

data = [
    {"region": "apac", "service": "recommendations", "latency_ms": 180.3, "uptime_pct": 97.193, "timestamp": 20250301},
    {"region": "apac", "service": "catalog", "latency_ms": 125.98, "uptime_pct": 98.59, "timestamp": 20250302},
    {"region": "apac", "service": "checkout", "latency_ms": 168.9, "uptime_pct": 98.913, "timestamp": 20250303},
    {"region": "apac", "service": "support", "latency_ms": 109.63, "uptime_pct": 97.418, "timestamp": 20250304},
    {"region": "apac", "service": "catalog", "latency_ms": 128.36, "uptime_pct": 97.901, "timestamp": 20250305},
    {"region": "apac", "service": "catalog", "latency_ms": 179.25, "uptime_pct": 99.319, "timestamp": 20250306},
    {"region": "apac", "service": "support", "latency_ms": 135.47, "uptime_pct": 99.258, "timestamp": 20250307},
    {"region": "apac", "service": "payments", "latency_ms": 144, "uptime_pct": 98.321, "timestamp": 20250308},
    {"region": "apac", "service": "support", "latency_ms": 140.19, "uptime_pct": 99.149, "timestamp": 20250309},
    {"region": "apac", "service": "support", "latency_ms": 100.06, "uptime_pct": 97.34, "timestamp": 20250310},
    {"region": "apac", "service": "analytics", "latency_ms": 188.96, "uptime_pct": 98.381, "timestamp": 20250311},
    {"region": "apac", "service": "payments", "latency_ms": 113.74, "uptime_pct": 97.992, "timestamp": 20250312},
    {"region": "emea", "service": "checkout", "latency_ms": 198.89, "uptime_pct": 98.641, "timestamp": 20250301},
    {"region": "emea", "service": "catalog", "latency_ms": 204.55, "uptime_pct": 99.326, "timestamp": 20250302},
    {"region": "emea", "service": "catalog", "latency_ms": 189.89, "uptime_pct": 98.004, "timestamp": 20250303},
    {"region": "emea", "service": "recommendations", "latency_ms": 113.89, "uptime_pct": 98.503, "timestamp": 20250304},
    {"region": "emea", "service": "recommendations", "latency_ms": 179.89, "uptime_pct": 98.844, "timestamp": 20250305},
    {"region": "emea", "service": "support", "latency_ms": 159.34, "uptime_pct": 98.932, "timestamp": 20250306},
    {"region": "emea", "service": "recommendations", "latency_ms": 163.63, "uptime_pct": 98.663, "timestamp": 20250307},
    {"region": "emea", "service": "payments", "latency_ms": 137.3, "uptime_pct": 97.186, "timestamp": 20250308},
    {"region": "emea", "service": "recommendations", "latency_ms": 222.45, "uptime_pct": 98.448, "timestamp": 20250309},
    {"region": "emea", "service": "recommendations", "latency_ms": 194.79, "uptime_pct": 99.359, "timestamp": 20250310},
    {"region": "emea", "service": "payments", "latency_ms": 217.03, "uptime_pct": 97.663, "timestamp": 20250311},
    {"region": "emea", "service": "recommendations", "latency_ms": 187.65, "uptime_pct": 97.43, "timestamp": 20250312},
    {"region": "amer", "service": "payments", "latency_ms": 170.06, "uptime_pct": 99.139, "timestamp": 20250301},
    {"region": "amer", "service": "payments", "latency_ms": 237.7, "uptime_pct": 99.008, "timestamp": 20250302},
    {"region": "amer", "service": "catalog", "latency_ms": 150.55, "uptime_pct": 99.197, "timestamp": 20250303},
    {"region": "amer", "service": "analytics", "latency_ms": 151.27, "uptime_pct": 98.814, "timestamp": 20250304},
    {"region": "amer", "service": "recommendations", "latency_ms": 210.53, "uptime_pct": 99.207, "timestamp": 20250305},
    {"region": "amer", "service": "analytics", "latency_ms": 157.45, "uptime_pct": 98.482, "timestamp": 20250306},
    {"region": "amer", "service": "support", "latency_ms": 179.26, "uptime_pct": 98.097, "timestamp": 20250307},
    {"region": "amer", "service": "support", "latency_ms": 171.97, "uptime_pct": 97.611, "timestamp": 20250308},
    {"region": "amer", "service": "catalog", "latency_ms": 195.7, "uptime_pct": 99.46, "timestamp": 20250309},
    {"region": "amer", "service": "support", "latency_ms": 143.78, "uptime_pct": 97.577, "timestamp": 20250310},
    {"region": "amer", "service": "support", "latency_ms": 186.52, "uptime_pct": 98.416, "timestamp": 20250311},
    {"region": "amer", "service": "checkout", "latency_ms": 132.63, "uptime_pct": 99.302, "timestamp": 20250312}
]

@app.post("/api/latency")
def analyze_latency(request: AnalyticsRequest):
    results = {}
    for region in request.regions:
        region_data = [r for r in data if r.get("region") == region]
        if not region_data:
            continue
        latencies = [r["latency_ms"] for r in region_data]
        uptimes = [r["uptime_pct"] for r in region_data]
        avg_latency = statistics.mean(latencies)
        sorted_latencies = sorted(latencies)
        p95_index = int(len(sorted_latencies) * 0.95)
        p95_latency = sorted_latencies[p95_index]
        avg_uptime = statistics.mean(uptimes)
        breaches = sum(1 for lat in latencies if lat > request.threshold_ms)
        results[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": breaches
        }
    return results