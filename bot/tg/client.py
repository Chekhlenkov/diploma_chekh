from typing import Any

import requests

from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse
from todolist import settings
from pydantic import ValidationError


class TgClient:
    def __init__(self, token: str | None = None) -> None:
        self.__token = token if token else settings.BOT_TOKEN
        self.__base_url = f"https://api.telegram.org/bot{self.__token}/"

    """ Получение ботом исходящих сообщений от пользователя """
    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        data = self._get('getUpdates', offset=offset, timeout=timeout)
        return GetUpdatesResponse(**data)

    """ Получение пользователем сообщений от бота """
    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        data = self._get('sendMessage', chat_id=chat_id, text=text)
        return SendMessageResponse(**data)

    """ URL для запроса к Telegram боту через токен """
    def __get_url(self, method: str) -> str:
        return f'{self.__base_url}{method}'

    """Метод запроса и проверка корректности ответа от Django"""
    def _get(self, command: str, **params: Any) -> dict:
        url = self.__get_url(command)
        response = requests.get(url, params=params)
        if not response.ok:
            print(f'Invalid status code from telegram {response.status_code} on command {command}')
            return {'ok': False, 'result': []}
        return response.json()

    def _serialize_response(self, serializer_class, data):
        try:
            return serializer_class(**data)
        except ValidationError as e:
            print(f'Failed to serializer telegram response due {e}')
            raise ValueError

