from fastapi import FastAPI, HTTPException, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from storage_factory import get_storage_api
from config import config

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize storage API
storage_api = get_storage_api(config["OBJECT_STORAGE_SERVICE"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "storage_service": config["OBJECT_STORAGE_SERVICE"],
        "endpoint": config["OBJECT_STORAGE_ENDPOINT"]
    }

@app.post("/bucket/create/{bucket_name}")
async def create_bucket(bucket_name: str):
    result = await storage_api.create_bucket(bucket_name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/bucket/{bucket_name}/upload")
async def upload_file(bucket_name: str, file: UploadFile = File(...)):
    result = await storage_api.upload_file(bucket_name, file)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/bucket/{bucket_name}/files")
async def list_files(bucket_name: str):
    result = await storage_api.list_files(bucket_name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/bucket/{bucket_name}/download/{filename}")
async def download_file(bucket_name: str, filename: str):
    result = await storage_api.download_file(bucket_name, filename)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # Just return the raw bytes
    return Response(content=result)

@app.delete("/bucket/{bucket_name}/file/{filename}")
async def delete_file(bucket_name: str, filename: str):
    result = await storage_api.delete_file(bucket_name, filename)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9090)