from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: int
    name: str
    first_name: str
    email: str
    profession: str | None = None

    model_config = ConfigDict(from_attributes=True)