class TokenValidationError(Exception):
    pass


class TokenNotFound(TokenValidationError):
    pass


class TokenAlreadyUsedError(TokenValidationError):
    pass


class TokeExpiredError(TokenValidationError):
    pass
