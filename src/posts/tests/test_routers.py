from fastapi import Response
from fastapi.testclient import TestClient

from ...main import app

client = TestClient(app)


def test_create_post():
    pass
