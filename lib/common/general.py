number = int | float

def clamp(value: number, min: number, max: number):
    if value < min:
        return min
    elif value > max:
        return max
    return value

def clamp_abs(value: number, distance: number):
    if distance < 0:
        raise Exception("clamp_abs() requires a positive distance")
    if value < -distance:
        return -distance
    elif value > distance:
        return distance
    return value

