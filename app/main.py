from fastapi import FastAPI

from app.routes.events import event_router, search_router
from app.routes.user import auth_router
from app.routes.ticketing import ticketing_router
import uvicorn

app = FastAPI(
    title="EventO Management system"
)
app.include_router(auth_router)
app.include_router(event_router)
app.include_router(ticketing_router)
app.include_router(search_router)

# if __name__ == '__main__':
#     uvicorn.run(app, port=8080, host='0.0.0.0')