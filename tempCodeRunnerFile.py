def twos_comp_to_dec(binary_str):
    # Check if it's negative
    if binary_str[0] == "1":
        # 2's complement: invert + add 1
        inverted = "".join("1" if b == "0" else "0" for b in binary_str)
        decimal_value = int(inverted, 2) + 1
        return -decimal_value
    else:
        # Positive number
        return int(binary_str, 2)