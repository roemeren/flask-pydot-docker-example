"""
common.py

This module contains shared variables and utility functions
used across the Flask application for processing uploaded files.

Current Shared Variables:
- progress_data: A dictionary tracking the progress of file processing, 
  including:
  - 'progress': An integer representing the current progress percentage (0-100).
  - 'filename': A string containing the name of the currently processed file.

Usage:
Import this module in both `app.py` and `processing.py` to access and modify 
the shared `progress_data`.
"""

# Keep track of progress and filename
progress_data = {'progress': 0, 'filename': None}