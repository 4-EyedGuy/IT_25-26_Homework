def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return [result] * n
        return wrapper
    return decorator

@repeat(3)
def hello():
    return "end is never the "

print(hello())