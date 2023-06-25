from datetime import datetime
from typing import Dict

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from goals.models import Board
from goals.serializers import BoardParticipant, BoardSerializer
from tests.factories import BoardParticipantFactory, BoardFactory


@pytest.mark.django_db
class TestBoardView:
    url: str = reverse('goals:board_list')

    def test_board_create(self, client, auth_client):
        """ Тест на создание доски """
        url = reverse('goals:create_board')

        expected_response = {
            'created': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'updated': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'title': 'test board',
            'is_deleted': False
        }
        response = client.post(path=url, data=expected_response)

        assert response.status_code == status.HTTP_201_CREATED
        board = Board.objects.get()
        assert board.title == expected_response['title']
        assert response.data['is_deleted'] == expected_response['is_deleted']

    def test_board_list_deny(self, client) -> None:
        """ Неавторизованные пользователи не могут видеть список досок. """
        response: Response = client.get(self.url)

        assert (
                response.status_code == status.HTTP_403_FORBIDDEN
        ), "Отказ в доступе не предоставлен"

    def test_board_retrieve_not_participant(self, auth_client) -> None:
        """ Авторизованный пользователь не видит доску, если он не является участником"""
        board = BoardFactory(is_deleted=True)
        BoardParticipantFactory(board=board)
        url: str = reverse("goals:board_detail", kwargs={"pk": board.id})

        unexpected_response: Dict = BoardSerializer(board).data
        response: Response = auth_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND, "Запрос дал результат"
        assert not response.data == unexpected_response, "Получена чужая доска"

    def test_board_retrieve_deny(self, client) -> None:
        """ Неавторизованные пользователи не могут удалить доску """
        url: str = reverse("goals:board_detail", kwargs={"pk": 1})
        response: Response = client.get(url)

        assert (
                response.status_code == status.HTTP_403_FORBIDDEN
        ), "Отказ в доступе не предоставлен"
