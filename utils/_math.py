def to_number(s):
    try:
        return float(s)
    except ValueError:
        return None