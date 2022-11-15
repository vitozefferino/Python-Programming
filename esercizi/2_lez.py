def sum_list(my_list):
    if my_list:
        result = 0
        for item in my_list:
            result = result + item
        return result
    else:
        return None

my_list = [1, 2, 3, 4]
print("Risultato: {}" .format(sum_list(my_list)))