from typing import Dict, Union

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from goals.models import GoalCategory
from tests.factories import BoardFactory, BoardParticipantFactory


@pytest.mark.django_db
class TestCategoryCreateView:
    """Тесты для GoalCategory """
    url: str = reverse("goals:create_category")

    def test_category_create_owner_moderator(self, auth_client, user) -> None:
        """       Создание новой категории владельцем или модератором доски.        """
        board = BoardFactory()
        BoardParticipantFactory(board=board, user=user)

        create_data: Dict[str, Union[str, int]] = {
            "board": board.pk,
            "title": "Owner category",
        }

        response: Response = auth_client.post(self.url, data=create_data)
        created_category = GoalCategory.objects.filter(
            title=create_data["title"], board=board, user=user
        ).exists()

        assert response.status_code == status.HTTP_201_CREATED
        assert created_category, "Созданной категории не существует"

    def test_category_create_deleted_board(self, auth_client, user) -> None:
        """        Создание категории на удаленной доске.        """
        board = BoardFactory(is_deleted=True)
        BoardParticipantFactory(board=board, user=user)

        create_data: Dict[str, Union[str, int]] = {
            "board": board.pk,
            "title": "Deleted board category",
        }

        response = auth_client.post(self.url, data=create_data)
        unexpected_category = GoalCategory.objects.filter(
            title=create_data["title"], board=board, user=user
        ).exists()

        assert response.status_code == status.HTTP_400_BAD_REQUEST, "Отказ в доступе не предоставлен"
        assert response.json() == {'board': ['board is deleted']}, "Вы можете создать категорию"
        assert not unexpected_category, "Категория создана"

    def test_category_create_deny(self, client) -> None:
        """ Создание категории неавторизованным пользователем        """
        response: Response = client.post(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN, "Отказ в доступе не предоставлен"
