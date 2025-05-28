
from fastapi import FastAPI
from routes.item_routes import router as item_router
#from routes.user_routes import router as user_router
from routes.cart_routes import router as cart_router  
from routes.order_routes import router as order_router
from routes.payment_routes import router as payment_router


app = FastAPI(title="AWE Electronics API", version="1.0")

# Include routers
app.include_router(item_router, prefix="/items", tags=["items"])
#app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(cart_router, prefix="/cart", tags=["Cart"])  
app.include_router(payment_router, prefix="/payments", tags=["Payments"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AWE Electronics Backend"}
