from .commands import register_command_handlers
from .callbacks import register_callback_handlers
from .media import register_media_handlers

def register_all_handlers(app):
    register_command_handlers(app)
    register_callback_handlers(app)
    register_media_handlers(app)

__all__ = ["register_all_handlers", "register_command_handlers", "register_callback_handlers", "register_media_handlers"]
