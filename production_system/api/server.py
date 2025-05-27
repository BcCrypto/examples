import logging
import os
from datetime import datetime

from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.security import OAuth2PasswordBearer
from prometheus_client import start_http_server

from ..utils.metrics import get_metrics
from ..utils.github import report_issue
from ..wallet import get_balance, redeem_proof, transfer_tokens
from pydantic import BaseModel

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "trading.log"),
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def get_current_user(token: str = Depends(oauth2_scheme)):
    return token


@app.post("/github-update")
async def github_update_listener(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    if payload.get("action") == "opened" and payload.get("repository", {}).get("full_name") == "RFDX_admin/trading-algos":
        background_tasks.add_task(report_issue, "New issue opened", 0.95, datetime.utcnow().isoformat())
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return get_metrics()


@app.get("/secure-dashboard")
def secure_dashboard(user: str = Depends(get_current_user)):
    return {"message": f"Welcome, {user}. Dashboard is secure."}


class TransferRequest(BaseModel):
    target: str
    amount: int


class RedeemRequest(BaseModel):
    proof: str


@app.get("/wallet/balance")
def wallet_balance():
    return {"balance": get_balance()}


@app.post("/wallet/transfer")
def wallet_transfer(req: TransferRequest):
    ok, msg = transfer_tokens(req.target, req.amount)
    return {"ok": ok, "message": msg}


@app.post("/wallet/redeem")
async def wallet_redeem(req: RedeemRequest):
    await redeem_proof(req.proof)
    return {"status": "redeemed"}


def start_metrics_server(port: int = 8001):
    start_http_server(port)
