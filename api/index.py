from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import statistics

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Define the request body structure
class AnalyticsRequest(BaseModel):
    regions: list[str]
    threshold_ms: float

# Load the latency data
with open("q-vercel-latency.json", "r") as f:
    data = json.load(f)

@app.post("/")
def analyze_latency(request: AnalyticsRequest):
    results = {}
    
    for region in request.regions:
        # Filter records for this region
        region_data = [r for r in data if r.get("region") == region]
        
        if not region_data:
            continue
            
        # Extract latencies and uptimes
        latencies = [r["latency_ms"] for r in region_data]
        uptimes = [r["uptime_pct"] for r in region_data]
        
        # Calculate metrics
        avg_latency = statistics.mean(latencies)
        p95_latency = statistics.quantiles(latencies, n=20)[18]  # 95th percentile
        avg_uptime = statistics.mean(uptimes)
        breaches = sum(1 for lat in latencies if lat > request.threshold_ms)
        
        results[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": breaches
        }
    
    return results