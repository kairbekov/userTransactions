import async_asgi_testclient
import loguru
import pytest



@pytest.mark.asyncio
async def test_get_users(
        db,
        auth_api_client: async_asgi_testclient.TestClient,
):
    resp = await auth_api_client.get('/api/v1/users')
    assert resp.status_code == 200
    result = resp.json()
    for i in result:
        i.pop('id')
    expected = [
        {'name': 'default', 'surname': 'default', 'balance': None},
        {'name': 'abl', 'surname': 'dabl', 'balance': 100},
        {'name': 'hello', 'surname': 'world', 'balance': 0},
        {'name': 'test', 'surname': 'test', 'balance': 10},
    ]
    assert resp.status_code == 200
    assert all(user in expected for user in result)


@pytest.mark.asyncio
async def test_get_user_by_id(
        db,
        auth_api_client: async_asgi_testclient.TestClient,
):
    resp = await auth_api_client.get('/api/v1/users/1')
    result = resp.json()
    result.pop('id')
    assert resp.status_code == 200
    assert result == {
        'name': 'AdminFirst',
        'surname': 'AdminLast',
        'balance': 200
    }


@pytest.mark.asyncio
async def test_get_nonexistent_user(
        db,
        auth_api_client: async_asgi_testclient.TestClient,
):
    resp = await auth_api_client.get('/api/v1/users/99')
    assert resp.status_code == 404
    assert 'User with provided ID was not found' in resp.text


@pytest.mark.asyncio
async def test_delete_user(
        db,
        auth_api_client: async_asgi_testclient.TestClient,
):
    body = dict(id=2)
    resp = await auth_api_client.delete(
        '/api/v1/users',
        json=body)
    assert resp.status_code == 200

    resp1 = await auth_api_client.get('/api/v1/users/2')
    assert resp1.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_user(
        db,
        auth_api_client: async_asgi_testclient.TestClient,
):
    body = dict(id=99)
    resp = await auth_api_client.delete(
        '/api/v1/users',
        json=body
    )
    assert resp.status_code == 404
    assert 'User with provided ID was not found' in resp.text