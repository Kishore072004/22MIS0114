from fastapi import Request
import time
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_logger")

async def custom_logging_middleware(request: Request, call_next):
    """
    A simple logging middleware that tracks the time taken to process a request.
    It logs the HTTP Method, URL path, Status Code, and Processing Time.
    """
    start_time = time.time()
    
    # Pass the request to the main application
    response = await call_next(request)
    
    # Calculate the time it took
    process_time = time.time() - start_time
    
    # Log the details directly to the terminal
    logger.info(f"[{request.method}] {request.url.path} | Status: {response.status_code} | Time: {process_time:.4f}s")
    
    return response
