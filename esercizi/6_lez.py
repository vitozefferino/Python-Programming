class CSVFile:

    def __init__(self, name):
        
        if not isinstance(name,str):
            raise TypeError('Nome del file non stringa')
        
        # Setto il nome del file
        self.name = name
        
        # Provo ad aprirlo e leggere una riga
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e:
            self.can_read = False
            print('Errore in apertura del file: "{}"'.format(e))


    def get_data(self, start=None, end=None):

        # Check start/end        
        if start is not None:
            try:
                start = int(start)
            except:
                raise TypeError('Start non interpretabile come intero ("{}")'.format(start))
            if start <= 0:
                raise ValueError('Start minore o uguale a zero ("{}")'.format(start))
        if end is not None:
            try:
                end = int(end)
            except:
                raise TypeError('Start non interpretabile come intero ("{}")'.format(end))
            if end <= 0:
                raise ValueError('End minore o uguale a zero ("{}")'.format(end))

        if start is not None and end is not None and start > end:
            raise ValueError('Start maggiore di end! start="{}", end="{}"'.format(start,end))         
        
        if not self.can_read:
            
            # Se nell'init ho settato can_read a False vuol dire che
            # il file non poteva essere aperto o era illeggibile
            print('Errore, file non aperto o illeggibile')
            
            # Esco dalla funzione tornando "niente".
            return None

        else:
            # Inizializzo una lista vuota per salvare tutti i dati
            data = []
    
            # Apro il file
            my_file = open(self.name, 'r')

            # Leggo il file linea per linea
            for i, line in enumerate(my_file):
                
                # Faccio lo split di ogni linea sulla virgola
                elements = line.split(',')
                
                elements[-1] = elements[-1].strip()
    
                # Se NON sto processando l'intestazione...
                if elements[0] != 'Date':
                    
                    # Aggiungo alla lista gli elementi di questa linea se devo
                    if start is not None and end is None:
                        if i+1 >= start:
                            data.append(elements)
                    elif end is not None and start is None:
                        if i+1 <= end:
                            data.append(elements)
                    elif start is not None and end is not None:
                        if i+1 >= start and i+1 <= end:
                            data.append(elements)  
                    else:
                        data.append(elements)

            if start is not None and start > i:
                raise ValueError('Start maggiore del totale delle righe del file (end="{}", righe="{}"'.format(start, i))
            
            if end is not None and end > i:
                raise ValueError('End maggiore del totale delle righe del file (end="{}", righe="{}"'.format(end, i))

            my_file.close()
            
            return data