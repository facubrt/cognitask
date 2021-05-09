def singleton (cls):
    instances = dict()

    def wrap(*arg, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*arg, **kwargs)
        
        return instances[cls]
        
    return wrap