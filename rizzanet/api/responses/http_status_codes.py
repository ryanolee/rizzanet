'''Index of status codes for rizzanet API'''
class http_status:
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    NOT_MODIFIED = 304
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    GONE = 410
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503

    ERROR_MESSAGE_ALIASES = {
        INTERNAL_SERVER_ERROR : 'Error: internal server error.'
    }

    @classmethod
    def get_error_message(cls, code):
        '''Returns defualt error messages for error codes passed to it'''
        if not code in cls.ERROR_MESSAGE_ALIASES:
            return ''
        return cls.ERROR_MESSAGE_ALIASES[code]

