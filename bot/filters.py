from aiogram.types import Message
from aiogram.filters import BaseFilter
from postgres_functions import check_user_in_table


class PRE_START(BaseFilter):
    async def __call__(self, message: Message):
        data = await check_user_in_table(message.from_user.id)
        if data:
            return False
        return True

letter_kit = 'abcdefghijklmnopqrstuvwxyzöäüß'

class IS_LETTER(BaseFilter):
    async def __call__(self, message: Message):
        for letter in message.text.strip().lower():
            if letter not in letter_kit:
                return False
        return True