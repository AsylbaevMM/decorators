import functools


class MaxCallsException(Exception):
    """Custom exception for 'limited_calls' decorator, raises if number of calls exceeded"""
    pass
    

class limited_calls:
    """Decorator that specifies the allowed number of function calls.
    Takes one argument: n - allowed number of function calls.
    """ 
      
    def __init__(self, n):
        self.n = n
        self.maximum = n
        
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.n > 0:
                self.n -= 1
                return func(*args, **kwargs)  
            raise MaxCallsException(f"Number of calls exceeded({self.maximum})")
        return wrapper
    

class takes_numbers:
    """Decorator checking that all args and kwargs are instances of int and float types"""
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        
    def __call__(self, *args, **kwargs):
        if all([type(i) in [int, float] for i in args]) and all([type(i) in [int, float] for i in kwargs]):
            return self.func(*args, **kwargs)
        raise TypeError("Arguments must be int or float")


class returns:
    """Decorator checking that the return value of the function is instance of datatype.
    Takes one argument: datatype - type of return value"""
    def __init__(self, datatype):
        self.datatype = datatype
        
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if type(result) == self.datatype:
                return result
            raise TypeError
        return wrapper
    

class ignore_exception:
    """a decorator that takes an arbitrary number of positional arguments - exception types, and displays the text "Exception 'name' handled" 
    if an exception belonging to one of the passed types was raised during the execution of the decorated function. 
    If the thrown exception does not belong to any of the passed types, it is raised again."""
    def __init__(self, *exceptions):
        self.exceptions = exceptions
        
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result =  func(*args, **kwargs)
                return result
            except Exception as err:
                if type(err) in self.exceptions:
                    print(f'Exception {type(err).__name__} handled')
                else:
                    raise err                  
        return wrapper


class type_check:
    """A decorator that checks that the types of all positional arguments passed to the function being decorated fully map to types in the types list, 
    i.e. the type of the first argument is the first element of the types list, 
    the type of the second argument is the second element of the types list, and so on. 
    If this condition is not met, a TypeError exception is raised.
    Take one argument: types - a list whose elements are data types """
    def __init__(self, types):
        self.types = types
        
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if all(map(lambda x: type(x[0]) == x[1], zip(args, self.types))):
                return func(*args, **kwargs)
            raise TypeError
        return wrapper
    

class predicate:
    """A decorator that allows you to conveniently combine predicates using the &, | and ~.
    example:
    @predicate
    def is_equal(a, b):
        return a == b

    @predicate
    def is_less_than(a, b):
        return a < b

    print((is_less_than | is_equal)(1, 2))        # True; equals is_less_than(1, 2) or is_equal(1, 2)"""
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func


    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)  


    def __and__(self, other):
        def result(*args, **kwargs):
            return self(*args, **kwargs) and other(*args, **kwargs)
        return result
    
    def __or__(self, other):
        def result(*args, **kwargs):
            return self(*args, **kwargs) or other(*args, **kwargs)
        return result      

    def __invert__(self):
        def result(*args, **kwargs):
            return not self.func(*args, **kwargs) 
        return predicate(result)   