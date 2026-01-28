from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import statistics

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# Define the request body structure
class AnalyticsRequest(BaseModel):
    regions: list[str]
    threshold_ms: float

# IMPORTANT: Embed your JSON data here since Vercel can't read files
# Replace this with your actual data from q-vercel-latency.json
data = [
    # Copy and paste your JSON array here
    # Example:
    # {"region": "apac", "latency_ms": 150, "uptime_pct": 99.5},
    # {"region": "apac", "latency_ms": 180, "uptime_pct": 99.2},
    # etc...
]

@app.get("/")
def read_root():
    return {
        "message": "Analytics endpoint is running. Send POST requests to this URL.",
        "usage": "POST with JSON body: {\"regions\": [\"apac\", \"emea\"], \"threshold_ms\": 176}"
    }

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
        # For 95th percentile, sort and get the value at 95% position
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