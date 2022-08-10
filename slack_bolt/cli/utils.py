from typing import Callable, Any


def handle_exception() -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                print("Shutdown requested... goodbye!")
            except Exception as e:
                print(e)
                exit()

        return wrapper

    return decorator
