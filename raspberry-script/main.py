import os
import aranet4
import pandas as pd

from google.cloud import bigquery
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = custom path

NUM_RETRIES = 3
CURRENT_DEVICE_ID = os.getenv('IDENTIFICADOR_RASPBERRY')
LOGS = []

client = bigquery.Client('e3escoles')


def get_devices_to_fetch() -> list:
    QUERY = f"""
        SELECT sensor, mac
        FROM `e3escoles.sensors.atribucio_dispositius`
        WHERE id_dispositiu = '{CURRENT_DEVICE_ID}'
        """
    
    query_job = client.query(QUERY)
    results = query_job.result()

    devices = {}
    for row in results:
        devices[row.sensor] = row.mac

    return devices


def get_last_database_entry(sensorId: str):
    global client
    QUERY = f"""
        SELECT MAX(data) as last_entry
        FROM `e3escoles.sensors.sensor_data`
        WHERE sensor = '{sensorId}'
        """
    
    query_job = client.query(QUERY)
    results = query_job.result()

    for row in results:
        if (row[0] != None):
            return pd.to_datetime(row[0])
    
    return pd.to_datetime('1950-01-01 00:00:00')


def upload_to_database(data: list, sensorId: str) -> bool:
    global client
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)

    # Filter the dataframe to only keep the records that are newer than the last one in the database
    last_entry = get_last_database_entry(sensorId)
    df = df[df['date'] > last_entry]

    if len(df) == 0:
        log_to_database('info', 'No new records to upload')
        return False

    df['sensor'] = sensorId

    df = df.rename(columns={
        'date': 'data',
        'temperature': 'temperatura',
        'humidity': 'humitat',
        'pressure': 'pressio',
        'co2': 'co2'
    })

    print (df.head(3))

    job = client.load_table_from_dataframe(df, 'e3escoles.sensors.sensor_data')
    job.result()
    log_to_database('info', 'Uploaded ' + str(len(df)) + ' records from device')
    return True


def log_to_database(type: str, message: str, error: str = '') -> bool:
    log = {
        "data": datetime.now(),
        "id_dispositiu": CURRENT_DEVICE_ID,
        "tipus": type,
        "missatge": message,
        "error": error
    }

    LOGS.append(log)
    
    log_msg = f'[{log["data"].strftime("%Y-%m-%d %H:%M:%S")}] ({log["id_dispositiu"]}) - {log["tipus"]} {log["missatge"]}'
    if log["error"] != '':
        log_msg += ' | ' + str(log["error"])

    print(log_msg)

    return True


def main():
    DEVICES_TO_FETCH = get_devices_to_fetch()
    log_to_database('info', 'Found ' + str(len(DEVICES_TO_FETCH)) + ' devices to fetch')

    for id, mac in DEVICES_TO_FETCH.items():
        current_try = 0
        success = False
        log_to_database('info', 'Fetching data from sensor with id ' + id + ' and mac ' + mac)

        while not success and current_try < NUM_RETRIES:
            try:
                history_data = aranet4.client.get_all_records(mac, {})
                success = True
            except Exception as e: 
                log_to_database('error', 'An error occurred while trying to get data from device, retry number '+ str(current_try), e)
                current_try += 1

        if (success):
            log_to_database('info', 'Got ' + str(history_data.records_on_device) + ' records from device ' + history_data.name)
            upload_to_database(history_data.value, id)
        else:
            log_to_database('alert', 'Could not get data from device ' + id)

        print ()

    if len(LOGS) > 0:
        df = pd.DataFrame(LOGS)
        job = client.load_table_from_dataframe(df, 'e3escoles.sensors.logs')
        job.result()
        print('Uploaded ' + str(len(LOGS)) + ' logs to database')

if __name__ == '__main__':
    main()