
from pydantic import BaseModel, Field


class PlayerStats(BaseModel):
    player: str
    team: str
    rating: float
    adr: float
    kast: float
    kd: float
    headshot: float


class PlayerAnalysis(BaseModel):
    player: str
    overview: str
    strengths: list[str] = Field(
        description="選手的主要優勢"
    )
    weaknesses: list[str] = Field(
        description="選手的弱點或需要觀察的地方"
    )
    conclusion: str

class PlayerAnalysis(BaseModel):
    player_name: str = Field(description="選手名稱")
    overall_assessment: str = Field(description="整體表現分析")
    strengths: list[str] = Field(description="選手的主要優勢")
    weaknesses: list[str] = Field(description="值得改善的地方")
    recent_form: str = Field(description="近期表現與趨勢")
    conclusion: str = Field(description="分析總結")
