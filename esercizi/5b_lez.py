class CSVFile: 
    def __init__(self, name):
            self.name = name
    def get_data(self):
        data = []
        try:
            my_file = open(self.name, 'r')
            for line in my_file:
                elements = line.split(',')
                if elements[0] != 'Date':
                    data.append(elements)
            my_file.close()
            return data
        except Exception:
            print('Errore: "{}".'.format(self.name))
            
class NumericalCSVFile(CSVFile):
    def get_data(self):
        data = super().get_data()
        numerical_data=[]
        if data != None:
            try:
                for item in data:
                    for i in range(1, len(item)): 
                        try:
                            item[i]=float(item[i])
                            numerical_data.append(item)
                        except ValueError:
                            print('Ho avuto un errore di VALORE. "item[1]" valeva "{}"'.     format((item[1])))
                        except TypeError:
                            print('Ho avuto un errore di TIPO. "item[1]" valeva "{}"'. format(type(item[1])))
                        except Exception as e:
                            print('Ho avuto un errore generico. "{}"'. format(e))
            except Exception:
                print('Errore. Il file da cui voglio estrarre i dati numerici non esiste')
        return numerical_data


my_file = NumericalCSVFile('shampoo_sales.csv')
print(my_file.get_data())