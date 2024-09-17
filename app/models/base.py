import datetime
from datetime import timezone

from sqlalchemy import Integer, String, DateTime, Column, func

from app.utils import generate_uid

class ModelBase:

    id = Column(Integer, primary_key=True)
    uid = Column(String, default=generate_uid())
    created_at = Column(DateTime, default=datetime.datetime.now(timezone.utc))
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def save(self):
        ...
