from pydantic import Basemodel


class Chat(Basemodel):
    id: int
    username: str


class Message(Basemodel):
    chat: Chat
    text: str | None


class UpdateObj(Basemodel):
    update_id: int
    message: Message


class SendMessageResponse(Basemodel):
    ok: bool
    result: Message


class GetUpdatesResponse(Basemodel):
    ok: bool
    result: list[UpdateObj]