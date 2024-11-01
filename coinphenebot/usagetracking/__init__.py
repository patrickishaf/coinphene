import sentry_sdk
import config

def init_tracking():
    sentry_sdk.init(
        dsn=config.sentry_url,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )


def send_event(message: str, key: str = "log_event", **kwargs):
    sentry_sdk.capture_event({
        "message": message,
        "level": "info",
        "extra": {
            "custom_key": key,
            "more_data": kwargs,
        }
    })