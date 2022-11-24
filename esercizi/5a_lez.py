class CSVFile():

    def __init__(self, name):
        self.name = name

    def get_data(self):
        elements = []  # this contains one line at time
        final = []    # this contains all the lists

        try:
            my_file = open(self.name, 'r')
        except Exception as e:
            print('Errore: "{}"'.format(e))
            
        my_file.readline()
        
        for line in my_file:
            elements = line.strip('\n').split(',')
            final.append(elements)
        my_file.close()
        
        if (len(final) == 0):
            return []
        else:
            return final

csv_file = CSVFile('shampoo_sales.csv')
print(csv_file.get_data())