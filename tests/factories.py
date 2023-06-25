from datetime import *
from django.utils import timezone

import factory.django
from core.models import User
from pytest_factoryboy import register

from django.contrib.auth import get_user_model

from goals.models import GoalCategory, Board, Goal, GoalComment, BoardParticipant
from bot.models import TgUser

USER_MODEL = get_user_model()


@register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs) -> User:
        return User.objects.create_user(*args, **kwargs)


class SignUpRequest(factory.DictFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')
    password_repeat = factory.LazyAttribute(lambda o: o.password)


class DatesFactoryMixin(factory.django.DjangoModelFactory):

    class Meta:
        abstract = True

    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)


# ============================================================
@register
class BoardFactory(DatesFactoryMixin):
    title = factory.Faker('sentence')

    class Meta:
        model = Board

    @factory.post_generation
    def with_owner(self, create, owner, **kwargs):
        if owner:
            BoardParticipant.objects.create(board=self, user=owner, role=BoardParticipant.Role.owner)


@register
class BoardParticipantFactory(DatesFactoryMixin):
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = BoardParticipant


@register
class GoalCategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('catch_phrase')
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = GoalCategory


@register
class GoalFactory(DatesFactoryMixin):
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(GoalCategoryFactory)
    title = factory.Faker('catch_phrase')

    class Meta:
        model = Goal


@register
class GoalCommentFactory(DatesFactoryMixin):
    user = factory.SubFactory(UserFactory)
    goal = factory.SubFactory(GoalFactory)
    text = factory.Faker('sentence')

    class Meta:
        model = GoalComment


@register
class CategoryFactory(factory.django.DjangoModelFactory):
    title = 'New Category'
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = GoalCategory
