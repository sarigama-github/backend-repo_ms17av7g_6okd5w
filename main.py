import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents
from schemas import Announcement, Work

app = FastAPI(title="Komunitas Karya Ilmiah Remaja API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend KIR aktif"}

@app.get("/api/hello")
def hello():
    return {"message": "Halo dari backend API!"}

# Public feed endpoints
@app.get("/api/announcements")
def list_announcements(limit: int = 20):
    try:
        items = get_documents("announcement", {}, limit)
        # Convert ObjectId to string for JSON if present
        for it in items:
            if "_id" in it:
                it["id"] = str(it.pop("_id"))
        return {"data": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/works")
def list_works(limit: int = 50, q: Optional[str] = None):
    try:
        filt = {}
        if q:
            # simple contains filter on title or author using regex
            import re
            filt = {"$or": [
                {"title": {"$regex": re.escape(q), "$options": "i"}},
                {"author": {"$regex": re.escape(q), "$options": "i"}},
            ]}
        items = get_documents("work", filt, limit)
        for it in items:
            if "_id" in it:
                it["id"] = str(it.pop("_id"))
        return {"data": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Submission models for requests
class AnnouncementIn(Announcement):
    pass

class WorkIn(Work):
    pass

# Create endpoints
@app.post("/api/announcements")
def create_announcement(payload: AnnouncementIn):
    try:
        new_id = create_document("announcement", payload)
        return {"id": new_id, "message": "Pengumuman dibuat"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/works")
def create_work(payload: WorkIn):
    try:
        new_id = create_document("work", payload)
        return {"id": new_id, "message": "Karya berhasil diunggah"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
