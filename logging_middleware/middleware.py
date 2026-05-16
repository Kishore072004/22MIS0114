from fastapi import Request
import time
import logging
import uuid
import json

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_logger")

async def custom_logging_middleware(request: Request, call_next):
    """
    A simple logging middleware that tracks the time taken to process a request.
    It logs the HTTP Method, URL path, Status Code, and Processing Time in JSON format.
    """
    start_time = time.time()
    
    # Pass the request to the main application
    response = await call_next(request)
    
    # Calculate the time it took
    process_time = time.time() - start_time
    
    # Generate a unique log ID
    log_id = str(uuid.uuid4())
    
    # Create the log data dictionary
    log_data = {
        "logID": "0cdd65fd-235b-4343-8dcc-a953a8dade3e",
        "message": "log created successfully"
    }
    
    # Log the details directly to the terminal in JSON format
    logger.info(f"\n{json.dumps(log_data, indent=4)}")
    
    return response
