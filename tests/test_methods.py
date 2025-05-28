import pytest
import time
from datetime import timedelta, datetime
from backend.security import SecurityManager, EndpointVerification
import jwt
from fastapi import HTTPException
from backend.ml_utils import map_dummy_variable

sm = SecurityManager()

def test_hash_and_verify_password():
    password = "mysecret123"
    hashed = sm.HashPassword(password)
    assert hashed != password
    assert sm.VerifyPassword(password, hashed)
    assert not sm.VerifyPassword("wrongpass", hashed)

def test_create_jwt_token_and_decode():
    data = {"sub": "user123"}
    token = sm.CreateJWTToken(data, expires_delta=timedelta(seconds=2))
    decoded = jwt.decode(token, sm.SECRET_KEY, algorithms=[sm.ALGORITHM], audience=sm.AUDIENCE, issuer=sm.ISSUER)
    assert decoded["sub"] == "user123"
    assert "exp" in decoded

def test_create_jwt_token_expiration():
    data = {"sub": "user123"}
    token = sm.CreateJWTToken(data, expires_delta=timedelta(seconds=1))
    time.sleep(2)  # Wait for token to expire
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(token, sm.SECRET_KEY, algorithms=[sm.ALGORITHM], audience=sm.AUDIENCE, issuer=sm.ISSUER)

def test_endpoint_verification_valid_token():
    data = {"sub": "user123"}
    token = sm.CreateJWTToken(data)
    # We simulate Dependency injection by calling function with token param
    payload = EndpointVerification(token=token)
    assert payload["sub"] == "user123"

def test_endpoint_verification_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        EndpointVerification(token="invalid.token.here")
    assert exc_info.value.status_code == 401

def test_map_dummy_variable():
    # Test exact matches (case-sensitive, no trimming)
    assert map_dummy_variable("<1H OCEAN") == [1, 0, 0, 0, 0]
    assert map_dummy_variable("INLAND") == [0, 1, 0, 0, 0]
    assert map_dummy_variable("ISLAND") == [0, 0, 1, 0, 0]
    assert map_dummy_variable("NEAR BAY") == [0, 0, 0, 1, 0]
    assert map_dummy_variable("NEAR OCEAN") == [0, 0, 0, 0, 1]

    # Test no match returns all zeros
    assert map_dummy_variable("UNKNOWN") == [0, 0, 0, 0, 0]

    # Test that partial or different case does not match
    assert map_dummy_variable("near bay") == [0, 0, 0, 0, 0]  # because lowercase doesn't match exactly
    assert map_dummy_variable("NEAR_BAY") == [0, 0, 0, 0, 0]  # underscore instead of space