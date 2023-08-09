import functools


def track_instances(cls):
    """The decorator adds an 'instances' attribute to the class being decorated, containing a list of all created instances of that class."""
    cls.instances = []
    old_init = cls.__init__
    
    @functools.wraps(old_init)
    def new_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        self.instances.append(self) 
    cls.__init__ = new_init
    return cls


def singleton(cls):
    """The decorator turns the class being decorated into a singleton."""
    cls.first = None
    old_new = cls.__new__
    
    @functools.wraps(old_new)
    def new_new(cls, *args, **kwargs):
        if cls.first is None:
            cls.first = object.__new__(cls)
        return cls.first
    cls.__new__ = new_new
    return cls


def auto_repr(args, kwargs):
    """A decorator provides a formal string representation(__repr__) for instances of the class being decorated.   
    The decorator takes two arguments in the following order:
    args - list of attribute names,
    kwargs - list of attribute names.
    If the attribute is listed in the args list, the string representation displays its value; 
    if the attribute is listed in the kwargs list, the value is displayed in the string representation along with the name."""
    def decorator(cls):        
        def custom_repr(cls):
            args_list = [repr(cls.__getattribute__(i)) for i in args]
            kwargs_list = [f"{i}={repr(cls.__getattribute__(i))}" for i in kwargs]
            result = f"{cls.__class__.__name__}({', '.join(args_list + kwargs_list)})"
            return result           
        cls.__repr__ = custom_repr
        return cls
    return decorator
        

def limiter(limit, unique, lookup):
    """Decorator with which you can limit the number of instances created by the decorated class to a certain number   
The decorator takes three arguments in the following order:

'limit' - the number of instances that the decorated class can create.

'unique' is the name of an instance attribute of the class being decorated, whose value is its identifier. 
Two instances with the same ID cannot exist. 
If an attempt is made to create an instance whose ID matches the ID of one of the previously created instances, 
that previously created instance must be returned.

'lookup' specifies which object should be returned if the limit has been exceeded and the value of the unique attribute has not been previously used. 
FIRST returns the very first instance created, LAST returns the most recent instance created"""
    instances = {}  
    def decorator(cls):      
        def inner(*args, **kwargs):
            obj = cls(*args, **kwargs)
            if getattr(obj, unique) in instances:
                return instances[getattr(obj, unique)]
            if len(instances) >= limit:
                if lookup == "LAST":
                    return instances[list(instances)[-1]]
                else:
                    return instances[list(instances)[0]]
            instances[getattr(obj, unique)] = obj
            return obj
        return inner
    return decorator