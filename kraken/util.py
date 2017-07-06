
def clean_locals(kwargs):
    ignore_keys = ('self',)
    ignore_values = (None,)
    return {
        k: v for k, v in kwargs.items()
        if k not in ignore_keys and v not in ignore_values
    }