import logging
import os
from datetime import datetime

import io
from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.security import OAuth2PasswordBearer
from prometheus_client import start_http_server

from ..utils.metrics import get_metrics
from ..utils.github import report_issue
from ..utils.state import get_env, get_latest_frame

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


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return """
    <html>
        <body>
            <h1>System Dashboard</h1>
            <h2>Metrics</h2>
            <pre id='metrics'></pre>
            <h2>Video Feed</h2>
            <img id='video' src='/video-feed' width='256' height='256'/>
            <script>
            async function updateMetrics(){
                const r = await fetch('/metrics');
                const m = await r.json();
                document.getElementById('metrics').textContent = JSON.stringify(m, null, 2);
            }
            setInterval(updateMetrics, 1000);
            updateMetrics();
            setInterval(function(){document.getElementById('video').src='/video-feed?'+Date.now();}, 1000);
            </script>
        </body>
    </html>
    """


@app.get("/video-feed")
def video_feed():
    frame = get_latest_frame()
    env = get_env()
    if frame is None and env is not None:
        frame = env.render("png")
    if frame is None:
        frame = b""
    return StreamingResponse(io.BytesIO(frame), media_type="image/png")


@app.get("/secure-dashboard")
def secure_dashboard(user: str = Depends(get_current_user)):
    return {"message": f"Welcome, {user}. Dashboard is secure."}


def start_metrics_server(port: int = 8001):
    start_http_server(port)
