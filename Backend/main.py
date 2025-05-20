from fastapi import FastAPI
from routes.product_routes import router as product_router

app = FastAPI(title="AWE Electronics API", version="1.0")

# Include product-related routes
app.include_router(product_router, prefix="/products", tags=["Products"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AWE Electronics Backend"}
