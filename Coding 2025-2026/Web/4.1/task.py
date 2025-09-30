def enforce_ints(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if not isinstance(arg, int):
                raise TypeError(f"{arg} немножко не int, иди исправляй")
        return func(*args, **kwargs)
    return wrapper

@enforce_ints
def mul(a, b):
    return a * b

print(mul(2, 5))
print(mul(2, "5"))