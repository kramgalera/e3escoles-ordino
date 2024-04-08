import google.cloud.bigquery as bigquery

TABLE_ATTRIBUTION_NOM = 'e3escoles.sensors.atribucio_dispositius'
TABLE_ATTRIBUTION = [
    bigquery.SchemaField("id_dispositiu", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("sensor", "STRING"),
    bigquery.SchemaField("mac", "STRING"),
]

TABLE_LOGS_NOM = 'e3escoles.sensors.logs'
TABLE_LOGS = [
    bigquery.SchemaField("data", "DATETIME", mode="REQUIRED"),
    bigquery.SchemaField("id_dispositiu", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("tipus", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("missatge", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("error", "STRING", mode="NULLABLE"),
]

TEMP_TABLE_DATA_NOM = 'e3escoles.sensors.sensor_data'
TEMP_TABLE_DATA = [
    bigquery.SchemaField("data", "DATETIME", mode="REQUIRED"),
    bigquery.SchemaField("sensor", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("temperatura", "FLOAT"),
    bigquery.SchemaField("humitat", "FLOAT"),
    bigquery.SchemaField("pressio", "FLOAT"),
    bigquery.SchemaField("co2", "FLOAT"),
]

client = bigquery.Client()

try:
    table = bigquery.Table(TABLE_ATTRIBUTION_NOM, schema=TABLE_ATTRIBUTION)
    client.create_table(table)
    print ("Created table", TABLE_ATTRIBUTION_NOM)

    # Insert ATTRIBUTION_LIST into the table
    # result = client.insert_rows(table, ATTRIBUTION_LIST)
    # print ("Inserted", len(ATTRIBUTION_LIST), "rows into", TABLE_ATTRIBUTION_NOM)
except Exception as e:
    print(e)

try:
    table = bigquery.Table(TABLE_LOGS_NOM, schema=TABLE_LOGS)
    client.create_table(table)
    print ("Created table", TABLE_LOGS_NOM)
except Exception as e:
    print(e)

try:
    table = bigquery.Table(TEMP_TABLE_DATA_NOM, schema=TEMP_TABLE_DATA)
    client.create_table(table)
    print ("Created table", TEMP_TABLE_DATA_NOM)
except Exception as e:
    print(e)
