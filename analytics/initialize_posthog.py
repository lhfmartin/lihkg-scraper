from contextlib import contextmanager
import uuid

import posthog


@contextmanager
def initialize_posthog():
    posthog.api_key = "phc_AuMRPTyC2ynoSiSfySiKynTmQiF5fxbuL9KUVT3FTV8Q"
    posthog.host = "https://eu.i.posthog.com"
    try:
        with posthog.new_context():
            posthog.identify_context(str(uuid.uuid4()))
            yield
    finally:
        posthog.shutdown()
