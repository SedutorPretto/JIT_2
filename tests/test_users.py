import pytest
import httpx
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch

from app.main import app


@pytest.mark.asyncio
async def test_get_user_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.get('/users/1')
    assert response.status_code == 200
    data = response.json()
    assert 'name' in data
    assert 'email' in data


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id", [-1, 0, "abc", 1.5, None])
async def test_get_user_invalid_input(user_id):
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.get(f'/users/{user_id}')
    assert response.status_code == 422
    data = response.json()
    assert 'detail' in data


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id", [9999, 10000, 123456])
async def test_get_user_not_found(user_id):
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.get(f'/users/{user_id}')
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == 'User not found'


@pytest.mark.asyncio
async def test_external_api_error():
    with patch('app.services.user_service.httpx.AsyncClient') as MockAsyncClient:
        mock_client_instance = MockAsyncClient.return_value.__aenter__.return_value
        mock_client_instance.get.side_effect = httpx.RequestError('Connection error', request=None)
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
            response = await ac.get('/users/1')
        assert response.status_code == 502
        data = response.json()
        assert data['detail'] == 'Error connecting to external API'
