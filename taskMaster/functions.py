def is_unique(data: list):
    ans = True
    for i in range(1, len(data)):
        if data[i-1] == data[i]:
            return False
    return ans
