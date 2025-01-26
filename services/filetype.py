import mimetypes
import os
import re
from urllib.parse import urlparse


def identify_type(input_value):
    # Check if it's a URL
    if re.match(r'^https?://', input_value):
        return "URL"

    if input_value.endswith(".pdf"):
        return "PDF File"
    elif input_value.endswith(".txt"):
        return "Text File"
    elif input_value.endswith('.doc', '.docx'):
        return "Word File"
    else:
        return "Unknown File Type"







