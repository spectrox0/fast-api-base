from sqlalchemy import Column, ForeignKey, String, Table

from config.database import Base

# Association table for favorite profiles
favorite_profiles = Table(
    "favorite_profiles",
    Base.metadata,
    Column("user_id", String, ForeignKey("users.id")),
    Column("profile_id", String, ForeignKey("profiles.id")),
)


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    user_id = Column(String, ForeignKey("users.id"))
