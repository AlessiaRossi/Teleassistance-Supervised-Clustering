# Teleassistance-Supervised-Clustering
English version, click [README.md](README.md).

## Indice
- [Configurazione dell'Ambiente](#configurazione-dellambiente)
- [Panoramica](#panoramica)

## Configurazione dell'Ambiente
Prima di eseguire il codice, è importante prendere alcune precauzioni e configurare correttamente l'ambiente. Segui questi passaggi:
1. Crea un Ambiente Virtuale:
   - Apri il terminale o il prompt dei comandi.
   - Esegui il seguente comando per creare un ambiente virtuale chiamato "venv": `python -m venv venv`
2. Attiva l'Ambiente Virtuale:
   - Se stai usando Windows: `.\venv\Scripts\activate`
   - Se stai usando Unix o MacOS: `source ./venv/Scripts/activate`
3. Disattiva l'Ambiente (Quando hai finito):
   - Usa il seguente comando per disattivare l'ambiente virtuale: `deactivate`
4. Installa le Dipendenze:
   - Dopo aver clonato il progetto e attivato l'ambiente virtuale, installa le dipendenze richieste usando: `pip install -r requirements.txt`
     Questo comando scarica tutti i moduli non standard necessari per l'applicazione.
5. Se la versione di Python utilizzata per generare l'ambiente virtuale non contiene una versione aggiornata di pip, aggiorna pip usando: `pip install --upgrade pip`
   
Una volta configurato l'ambiente virtuale e installate le dipendenze, sei pronto per eseguire l'applicazione. Semplicemente naviga al file `main.py` ed eseguilo.

## Panoramica
Questo progetto esplora l'integrazione dei servizi di teleassistenza con tecniche di clustering supervisionato.
- **Obiettivo**: Profilare i pazienti per comprendere il loro contributo all'aumento dei servizi di teleassistenza.
- **Focus Principale**: Identificare modelli e comportamenti comuni tra i pazienti legati all'aumento dell'uso della teleassistenza.
- **Approccio**:
  - Raggruppare i pazienti in base a modelli comuni o comportamenti simili relativi alla variabile target (`incremento_teleassistenze`).
  - Analizzare le differenze tra i gruppi di pazienti per determinare quali caratteristiche contribuiscono all'aumento della teleassistenza.
- **Metodi**:
  - Utilizzare tecniche avanzate di clustering che considerino sia le caratteristiche dei pazienti che la variabile di esito (`incremento_teleassistenze`).
