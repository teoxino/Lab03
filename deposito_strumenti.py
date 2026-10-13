
import csv
from operator import itemgetter


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le  strutture dati """
        self.nome = nome
        self._responsabile = responsabile
        self._strumenti = {}
        self._prestiti = {}
        self._ultimo_id_strumento = 0
        self._ultimo_id_prestito = 0

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, nuovo_responsabile):
        self._responsabile = nuovo_responsabile

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for riga in reader:
                    if not riga:
                        continue
                    id_str, tipo, marca, anno, valore = [x.strip() for x in riga]

                    self._strumenti[id_str] = {
                        'id_strumento': id_str,
                        'tipo': tipo,
                        'marca': marca,
                        'anno_acquisto': int(anno),
                        'valore': float(valore)
                    }

                    # Agiorna  contatore
                    num_id = int(id_str.replace('S', ''))
                    if num_id > self._ultimo_id_strumento:
                        self._ultimo_id_strumento = num_id
        except FileNotFoundError:
            raise FileNotFoundError(f"Errore: Il file '{file_path}' non esiste.")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        self._ultimo_id_strumento += 1
        nuovo_id = f"S{self._ultimo_id_strumento}"

        nuovo_strumento = {
            'id_strumento': nuovo_id,
            'tipo': tipo,
            'marca': marca,
            'anno_acquisto': int(anno_acquisto),
            'valore': float(valore)
        }

        self._strumenti[nuovo_id] = nuovo_strumento
        return f"{nuovo_id}, {tipo}, {marca}, {anno_acquisto}, {float(valore):.2f}"



    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        lista_strumenti = list(self._strumenti.values())
        strumenti_ordinati = sorted(lista_strumenti, key=itemgetter('marca'))

        # stampiamo in main
        return [
            f"{s['id_strumento']}, {s['tipo']}, {s['marca']}, {s['anno_acquisto']}, {s['valore']:.2f}"
            for s in strumenti_ordinati
        ]
    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        # Verifica se lo strumento esiste
        if id_strumento not in self._strumenti:
            raise Exception(f"Errore: Lo strumento '{id_strumento}' non è presente nel deposito.")

        for prestito in self._prestiti.values():
            if prestito['id_strumento'] == id_strumento:
                raise Exception(f"Errore: Lo strumento '{id_strumento}' è già in prestito.")

        self._ultimo_id_prestito += 1
        id_prestito = f"P{self._ultimo_id_prestito}"

        prestito = {
            'id_prestito': id_prestito,
            'data': data,
            'id_strumento': id_strumento,
            'cognome_allievo': cognome_allievo
        }
        self._prestiti[id_prestito] = prestito
        return f"[{id_prestito}] Data: {data} - Strumento: {id_strumento} - Allievo: {cognome_allievo}"

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        if id_prestito not in self._prestiti:
            raise Exception(f"Errore: Nessun prestito trovato con ID '{id_prestito}'.")

        del self._prestiti[id_prestito]