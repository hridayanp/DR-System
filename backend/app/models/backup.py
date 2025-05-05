from sqlalchemy import Column, Integer, String, DateTime, Text
from app.db.db import Base
from datetime import datetime, timezone

class Backup(Base):
    __tablename__ = 'backups'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    backup_url = Column(String, nullable=False)
    cloud_provider = Column(String, nullable=False)
    status = Column(String, default='Pending')
    error_message = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )
    
    updated_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return (
            f"<Backup(id={self.id}, user_id={self.user_id}, file_name='{self.file_name}', "
            f"cloud_provider='{self.cloud_provider}', status='{self.status}', created_at='{self.created_at}')>"
        )