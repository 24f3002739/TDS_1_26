from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import List

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Load the latency data
with open("q-vercel-latency.json", "r") as f:
    telemetry_data = json.load(f)

@app.post("/")
def analyze_latency(payload: dict):
    regions = payload.get("regions", [])
    threshold_ms = payload.get("threshold_ms", 180)
    
    results = {}
    
    for region in regions:
        # Filter records for this region
        region_records = [r for r in telemetry_data if r["region"] == region]
        
        if not region_records:
            continue
            
        # Calculate average latency
        latencies = [r["latency_ms"] for r in region_records]
        avg_latency = sum(latencies) / len(latencies)
        
        # Calculate 95th percentile
        sorted_latencies = sorted(latencies)
        p95_index = int(len(sorted_latencies) * 0.95)
        p95_latency = sorted_latencies[p95_index]
        
        # Calculate average uptime
        uptimes = [r["uptime_pct"] for r in region_records]
        avg_uptime = sum(uptimes) / len(uptimes)
        
        # Count breaches
        breaches = sum(1 for lat in latencies if lat > threshold_ms)
        
        results[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": breaches
        }
    
    return results