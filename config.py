"""
Configuration settings for AI Resume Analyzer & Career Assistant.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if available
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Upload and Security Limits
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "5"))
ALLOWED_EXTENSIONS = [".pdf"]

# Curated Technical & Professional Taxonomy for Skill Matching
COMMON_SKILLS = [
    # Programming Languages
    "python", "java", "c++", "c#", "javascript", "typescript", "go", "rust", "php", "ruby", "sql", "r",
    # Frameworks & Libraries
    "react", "angular", "vue", "django", "flask", "fastapi", "spring boot", "nodejs", "express",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "streamlit",
    # Databases & Storage
    "postgresql", "mysql", "mongodb", "redis", "sqlite", "oracle", "elasticsearch",
    # Cloud, DevOps & Tools
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "github", "linux", "ci/cd", "terraform",
    # Core CS Concepts & Methodologies
    "data structures", "algorithms", "object oriented programming", "oop", "system design",
    "agile", "scrum", "rest api", "graphql", "microservices", "unit testing"
]
