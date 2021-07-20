from pydantic import BaseModel


class CreateBrew(BaseModel):
    startOrStop: bool