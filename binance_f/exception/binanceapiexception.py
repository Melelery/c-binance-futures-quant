
class BinanceApiException(Exception):

    RUNTIME_ERROR = "RuntimeError"
    INPUT_ERROR = "InputError"
    KEY_MISSING = "KeyMissing"
    SYS_ERROR = "SysError"
    SUBSCRIPTION_ERROR = "SubscriptionError"
    ENV_ERROR = "EnvironmentError"
    EXEC_ERROR = "ExecuteError"

    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message
