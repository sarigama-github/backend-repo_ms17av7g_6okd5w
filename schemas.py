"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class Announcement(BaseModel):
    """
    Announcements for the youth science community
    Collection name: "announcement"
    """
    title: str = Field(..., description="Judul pengumuman")
    content: str = Field(..., description="Isi pengumuman / detail informasi")
    tags: Optional[List[str]] = Field(default=None, description="Tag terkait")
    author: Optional[str] = Field(default="Admin", description="Pembuat pengumuman")

class Work(BaseModel):
    """
    Youth scientific works (karya ilmiah remaja)
    Collection name: "work"
    """
    title: str = Field(..., description="Judul karya")
    author: str = Field(..., description="Nama penulis / tim")
    email: Optional[str] = Field(default=None, description="Kontak email")
    description: Optional[str] = Field(default=None, description="Deskripsi singkat karya")
    category: Optional[str] = Field(default=None, description="Bidang ilmu / kategori")
    file_url: Optional[HttpUrl] = Field(default=None, description="Link file (Google Drive, etc.)")
    thumbnail_url: Optional[HttpUrl] = Field(default=None, description="Gambar pratinjau (opsional)")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
