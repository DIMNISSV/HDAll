def get_month(old_m, old_y, add_m):
    need_m = (old_m + add_m) % 12
    if old_m + add_m > 12:
        old_y += 1
    if need_m == 0:
        old_y += 1
        need_m = 1
    return need_m, old_y
