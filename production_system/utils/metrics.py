from prometheus_client import Gauge

portfolio_gauge = Gauge('portfolio_value', 'Total portfolio value')
exposure_gauge = Gauge('risk_exposure', 'Current exposure level')


def get_metrics():
    return {
        'portfolio_value': portfolio_gauge._value.get(),
        'risk_exposure': exposure_gauge._value.get(),
    }
