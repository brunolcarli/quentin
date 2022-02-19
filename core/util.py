"""
Utilitaries and tools.
"""


def paginate(data, slice_size=5):
    """
    Chunks an list to paginate it.
    Default pagination size is 5.
    return: list of lists
    """
    for i in range(0, len(data), slice_size):
        yield data[i:i + slice_size]
