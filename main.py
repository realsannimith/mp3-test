from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

VOICES_DIR = "voices"

@app.get("/")
async def root():
    return {"message": "MP3 Server is running"}

@app.get("/{name}/{filename}")
async def get_mp3(name: str, filename: str):
    """
    Serve MP3 files from the voices directory for streaming
    Example: /name/hout_sok_reak_smey.mp3
    """
    # Construct the file path from voices directory
    file_path = os.path.join(VOICES_DIR, filename)
    
    # Check if file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check if it's an MP3 file
    if not filename.endswith('.mp3'):
        raise HTTPException(status_code=400, detail="Only MP3 files are supported")
    
    # Return FileResponse for streaming (no filename parameter to avoid download)
    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline"}
    )

@app.get("/list")
async def list_files():
    """List all available MP3 files"""
    try:
        files = [f for f in os.listdir(VOICES_DIR) if f.endswith('.mp3')]
        return {"files": files}
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Voices directory not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
