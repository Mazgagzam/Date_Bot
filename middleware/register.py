from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
import datetime

from db import db


class Register(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        if not db.is_there("users", "id", event.from_user.id):
            db.append_line(
                "users",
                [
                    event.from_user.id,
                    event.from_user.first_name,
                    event.from_user.username
                ],
            )

        user = db.select_class('users', 'id', event.from_user.id)
        user.username = event.from_user.username
        user.name = event.from_user.first_name

        if type(event) == Message:
            print(f"\033[34m{datetime.datetime.now()} - ID: {user.id} - Name: {user.name} - Text: {event.text}\033[0m")
        elif type(event) == CallbackQuery:
            print(f"\033[34m{datetime.datetime.now()} - ID: {user.id} - Name: {user.name} - Data: {event.data}\033[0m")

        data.update({"user": user})

        on_func = await handler(event, data)
        user()
        return on_func