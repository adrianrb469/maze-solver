import time


# Decorator function to calculate the time taken by a function to run
def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # get the current time
        result = func(*args, **kwargs)  # call the original function
        end_time = time.time()  # get the current time again
        elapsed_time = (
            end_time - start_time
        ) * 1000  # calculate the difference in milliseconds
        print(f"Function {func.__name__} took {elapsed_time} ms to run.")
        return result

    return wrapper


export = timer
