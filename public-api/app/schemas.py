from pydantic import BaseModel


class MemeBase(BaseModel):
    title: str
    description: str
    image_url: str  # Убедитесь, что это поле имеет тип str


class MemeCreate(MemeBase):
    pass


class MemeUpdate(MemeBase):
    pass


class Meme(MemeBase):
    id: int

    class Config:
        orm_mode = True
