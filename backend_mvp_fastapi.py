from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import random, json, os

app = FastAPI(title="Neo da Redação", version="0.1")

class RedacaoIn(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None

class CompetenceScore(BaseModel):
    nota: int
    justificativa: str

class RedacaoOut(BaseModel):
    c1: CompetenceScore
    c2: CompetenceScore
    c3: CompetenceScore
    c4: CompetenceScore
    c5: CompetenceScore
    total: int
    acoes: List[str]

@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1"}

@app.post("/score", response_model=RedacaoOut)
async def score_redacao(payload: RedacaoIn):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Texto vazio")

    # notas simuladas
    scores = [random.randint(120, 200) for _ in range(5)]
    justs = [
        "Justificativa competência 1",
        "Justificativa competência 2",
        "Justificativa competência 3",
        "Justificativa competência 4",
        "Justificativa competência 5",
    ]
    total = sum(scores)

    return {
        "c1": {"nota": scores[0], "justificativa": justs[0]},
        "c2": {"nota": scores[1], "justificativa": justs[1]},
        "c3": {"nota": scores[2], "justificativa": justs[2]},
        "c4": {"nota": scores[3], "justificativa": justs[3]},
        "c5": {"nota": scores[4], "justificativa": justs[4]},
        "total": total,
        "acoes": ["Revise ortografia", "Melhore argumentação"]
    }

@app.get("/exercicio")
async def get_exercicio():
    file = "redacoes.json"
    if not os.path.exists(file):
        raise HTTPException(status_code=404, detail="Nenhum exercício disponível")
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    modelo = random.choice(data)
    return modelo
