def sum_csv(file_name):
    elements = []    # splitted strings
    sum = 0   # sum value
    
    my_file = open(file_name, 'r')
    my_file.readline()
    for line in my_file:
        elements = line.split(',')
        value = elements[1]
        value = value.strip('\n')
        try:
            value = float(value)
            sum = sum + value
        except ValueError:
            pass
    my_file.close()
    if(len(elements)==0):
        return None
    else:
        return sum

print(sum_csv('shampoo_sales.csv'))