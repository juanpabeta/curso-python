from pydantic import BaseModel


class ConversionResponse(BaseModel):
    won: int
    lost: int
