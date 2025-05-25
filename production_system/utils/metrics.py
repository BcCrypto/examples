from prometheus_client import Gauge

portfolio_gauge = Gauge("portfolio_value", "Total portfolio value")
exposure_gauge = Gauge("risk_exposure", "Current exposure level")
# Estimated tokens consumed for transactions or LLM calls
token_tx_gauge = Gauge(
    "token_transaction_estimate", "Estimated token usage for recent operations"
)


def get_metrics():

    return {
        "portfolio_value": portfolio_gauge._value.get(),
        "risk_exposure": exposure_gauge._value.get(),
        "token_transaction_estimate": token_tx_gauge._value.get(),
    }


def set_token_estimate(value: float) -> None:
    """Update token transaction estimation gauge."""
    token_tx_gauge.set(value)

