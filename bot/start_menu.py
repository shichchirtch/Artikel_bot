from aiogram.types import BotCommand

# Функция для настройки кнопки Menu бота
async def set_main_menu(bot):
    # Создаем список с командами и их описанием для кнопки menu
    # bot
    main_menu_commands = [
        BotCommand(command='/zeigen',
                   description='Zeigen meine Worte'),

        BotCommand(command='/help',
                   description='Bot commands')
    ]

    await bot.set_my_commands(main_menu_commands)

