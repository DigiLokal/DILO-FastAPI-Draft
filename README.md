# DILO FastAPI 

This is a FastAPI project that provides an API for DigiLokal.

## Installation

1. Create a Python virtual environment:
   ```
   python -m venv env
   ```
   
2. Activate the virtual environment:
- On Windows:
  ```
  .\env\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source env/bin/activate
  ```

3. Install the project dependencies from requirements.txt:
  ```
  pip install -r requirements.txt
  ```
  
## Usage
1. Run the FastAPI server:
  ```
  uvicorn src.main:app --reload
  ```
  
2. Documentation
- API documentation and interactive UI can be accessed at http://127.0.0.1:8000/docs.
- Alternatively, you can explore the API endpoints using tools like Postman.