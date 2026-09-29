from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AnswerSync(BaseModel):
    question_id: str
    answer_json: str
    time_ms: int
    is_correct: bool

class StepSync(BaseModel):
    step_id: str
    points: int
    max_points: int
    attempts: int
    duration_ms: int
    mistakes_json: str

class AttemptSync(BaseModel):
    id: str
    module_code: str
    started_at: datetime
    submitted_at: datetime
    device_id: Optional[str]
    client_score: float
    app_version: Optional[str]
    answers: List[AnswerSync]
    steps: List[StepSync]

class MicroQuizResultSync(BaseModel):
    module_code: str
    day_offset: int
    score: float
    taken_at: datetime

class SyncPushRequest(BaseModel):
    attempts: List[AttemptSync]
    micro_quizzes: List[MicroQuizResultSync]

class CertResponse(BaseModel):
    id: str
    module_code: str
    score: float
    issued_at: datetime
    expires_at: datetime
    status: str
    payload_json: str
    signature_b64: str

class SyncPullResponse(BaseModel):
    certificates: List[CertResponse]
    content_version: int
