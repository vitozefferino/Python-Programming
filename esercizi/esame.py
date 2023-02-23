class ExamException(Exception):
    pass

class CSVTimeSeriesFile():
    def __init__(self, name):
        self.name = name
        # Provo ad aprirlo e leggere una riga
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception:
            self.can_read = False

    def get_data(self):
        if not self.can_read:
            # Se nell'init ho settato can_read a False vuol dire che il file non poteva essere aperto o era illeggibile
            raise ExamException("File non aperto o illeggibile")
        else:
            sorted = True
            has_duplicates = False
            data = []
            dates = []
            my_file = open(self.name, 'r')
            
            for line in my_file:
                elements = line.split(',')
                elements[-1] = elements[-1].strip()
                if elements[0] != 'Date':
                    # Controllo che la data sia valida
                    try:
                        if len(elements[0].split("-")) != 2:
                            continue
                        dates.append(elements[0])
                    except:
                        continue
                        
                    try:
                        # Controllo che il numero di passeggeri sia valido
                        elements[1] = int(elements[1])
                        if int(elements[1]) < 0:
                            continue
                    except:
                        continue

                    sorted = self.check_order(dates)
                    has_duplicates = self.check_duplicates(dates)
                    
                    if not sorted:
                        raise ExamException("Date non ordinate")
                    if has_duplicates:
                        raise ExamException("Una o più date duplicate")

                    data.append(elements)

            my_file.close()
            return data
                
    def check_order(self, list):
        prev_year = None
        prev_month = None
        for item in list:
            year, month = item.split("-")
            if prev_year is not None and int(year) < prev_year:
                return False
            elif prev_year is not None and int(year) == prev_year and int(month) < prev_month:
                return False
            prev_year = int(year)
            prev_month = int(month)
        return True

    def check_duplicates(self, list):
        # Inizializzo un insieme vuoto per tenere traccia degli elementi già visti
        seen = set()
        for elem in list:
            if elem in seen:
                return True
            seen.add(elem)
        return False

def detect_similar_monthly_variations(time_series, years):
    # Se years non è una lista o non contiene due elementi
    if not isinstance(years, list) or len(years) != 2:
        raise ExamException("Years deve essere una lista di due elementi")

    # Se years non contiene interi
    if not all(isinstance(year, int) for year in years):
        raise ExamException("Years deve contenere solo interi")

    # Se il primo anno è maggiore o uguale del secondo
    if years[0] >= years[1]:
            raise ExamException("Il primo anno deve essere minore del secondo")

    # Controllo che years contenga anni effettivamente presenti nella time_series
    time_series_years = {int(d[0][:4]) for d in time_series}
    for year in years:
        if year not in time_series_years:
            raise ExamException("Years contiene anni non validi")
        
    # Estraggo i dati dell'anno 1 dalla time series
    year1 = years[0]
    year1_data = [
        data_point for data_point in time_series
        if data_point[0].startswith(str(year1))
    ]

    # Estraggo i dati dell'anno 2 dalla time series
    year2 = years[1]
    year2_data = [
        data_point for data_point in time_series
        if data_point[0].startswith(str(year2))
    ]
    
    # Creo un dizionario per associare ogni mese all'indice della sua coppia nell'output
    month_pairs = {}
    for i in range(1, 12):
        month1 = str(i).zfill(2)
        month2 = str(i+1).zfill(2)
        key = month1 + '-' + month2
        value = i - 1
        month_pairs[key] = value
    
    # Creo un array di 11 elementi inizialmente a True
    output = [True] * 11

    # Calcolo la variazione tra ogni coppia di mesi per entrambi gli anni
    for month_pair, output_index in month_pairs.items():
        month1_data_year1 = None
        month2_data_year1 = None
        # Prendo i dati riguardanti il primo anno
        for d in year1_data:
            if d[0].endswith(month_pair[:2]):
                month1_data_year1 = d[1]
            elif d[0].endswith(month_pair[3:]):
                month2_data_year1 = d[1]
    
        variation_year1 = month2_data_year1 - month1_data_year1

        month1_data_year2 = None
        month2_data_year2 = None
        # Prendo i dati riguardanti il secondo anno
        for d in year2_data:
            if d[0].endswith(month_pair[:2]):
                month1_data_year2 = d[1]
            elif d[0].endswith(month_pair[3:]):
                month2_data_year2 = d[1]
    
        variation_year2 = month2_data_year2 - month1_data_year2
        
        # Confronto le due variazioni e aggiorna l'elemento corrispondente dell'output
        if abs(variation_year2 - variation_year1) > 2:
            output[output_index] = False
            
    return output