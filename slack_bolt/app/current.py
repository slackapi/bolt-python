import sys

if sys.version_info <= (3, 6):
    raise RuntimeError("Application sessions require Python 3.7.")
else:
    from contextvars import ContextVar

from slack_bolt.app import App


_current_app: ContextVar[App] = ContextVar(
    "_current_app", default=App()
)


def create_app(**kwargs) -> App:
    app = App(**kwargs)
    _current_app.set(app)
    return app


def get_app() -> App:
    return _current_app.get()


def set_app(app: App):
    """
    Set the given App in context var.
    This should only be called by the `App` itself. 
    """
    previous_app = _current_app.get()
    _current_app.set(app)
