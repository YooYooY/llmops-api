import logging
from functools import wraps
from types import FunctionType

from flask import jsonify

logging.basicConfig(level=logging.ERROR)


def json_response(code="success", message="OK", data=None, status=200):
    return jsonify({
        "code": code,
        "message": message,
        "data": data or {}
    }), status


def success(data=None, message="OK", status=200):
    return json_response("success", message, data, status)


def fail(message="Something went wrong", data=None, status=500):
    return json_response("fail", message, data, status)


def handle_exceptions(fn):
    """Route-level decorator for clean error responses."""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            # Log the real error, but return a safe message
            logging.exception(e)
            msg = str(e)

            # Friendly rewrites for common Weaviate issues
            lower = msg.lower()
            if "did not start up" in lower or "connection refused" in lower:
                return fail("Vector DB is not ready. Try again shortly.", status=503)
            if "no schema is present" in lower or "collection" in lower and "not found" in lower:
                return fail("Vector store is not initialized yet. Please add data first.", status=400)

            return fail("Internal server error.", status=500)

    return wrapper


def auto_handle_exceptions(ignore=None):
    """
    Class decorator: automatically applies `handle_exceptions`
    to every method of a class, except those listed in `ignore`.
    """
    ignore = ignore or []

    def decorator(cls):
        for name, attr in cls.__dict__.items():
            if isinstance(attr, FunctionType) and name not in ignore:
                setattr(cls, name, handle_exceptions(attr))
        return cls

    return decorator
