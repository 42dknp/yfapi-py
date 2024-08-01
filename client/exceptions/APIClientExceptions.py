# APIClientExceptions.py

class BaseAPIClientException(Exception):
    """Base class for api client exceptions."""
    pass


class APIClientException(BaseAPIClientException):
    """Exception for errors related to making requests to the api."""
    pass


class TransformerException(BaseAPIClientException):
    """Exception for authentication-related errors."""
    pass


class ValidatorException(BaseAPIClientException):
    """Exception for authorization-related errors."""
    pass


class ApiException(Exception):
    """Custom exception for API errors"""
    pass


class JSONDecodeError(Exception):
    """Custom exception for JSON errors"""
    pass
