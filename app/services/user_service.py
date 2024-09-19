import httpx
from typing import Dict


class ExternalAPIConnectionError(Exception):
    pass


async def get_user_data(user_id: int) -> Dict[str, str]:
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                raise ValueError('User not found')
            else:
                raise Exception('External API error')
        except httpx.RequestError as exc:
            raise ExternalAPIConnectionError('Error connecting to external API') from exc

    user_data = response.json()
    return {
        'name': user_data.get('name'),
        'email': user_data.get('email')
    }
