# Backend Design

### Basic Techniques

1. `fastapi` for API
2. use `SQLite` for portability

### Table Structure

tag_table: name

text_table: tag, desc, content, created, updated

### Usage

1. `pip install -r requirements.txt`
2. `uvicorn main:app --reload`
