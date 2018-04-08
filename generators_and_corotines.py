# Uma função geradora que imita o builtin range:
def my_range(n):
    i = 0
    while i < n:
        yield i
        i += 1


g = my_range(3)
print(next(g))
# Output: 0
print(next(g))
# Output: 1
print(next(g))
# Output: 2
# print(next(g))
# Raise StopIteration


g = my_range(3)
for i in my_range(10):
    print(i, end=" ")
print()
# Output: 0 1 2 3 4 5 6 7 8 9


# Uma função geradora que tanto retorna como aceita valores:
def hello():
    person = yield
    greeting = f"Hello, {person}!!!"
    yield greeting


def say_hello(name):
    hw = hello()
    next(hw)
    greeting = hw.send(name)
    print(greeting)


say_hello("Tonny")  # Prints 'Hello, Tonny!!!'
