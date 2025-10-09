"""
Controllers package
Contains HTTP request handlers (API endpoints)
"""
from .student_controller import router as student_router

__all__ = ["student_router"]

