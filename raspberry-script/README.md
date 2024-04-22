# Automatització de la recol·lecció de dades dels sensors Aranet

Fitxer de documentació de la implementació d'una Raspberry Pi per l'exportació de les dades de sensors Aranet4 a una base de dades BigQuery, a Google Cloud. Aquest document inclou totes les etapes necessàries per la configuració del Raspberry, sincronització amb els sensors i altres.

> Realitzat per [Andorra Recerca + Innovació](https://ari.ad), ultima actualització: Març 2024.


## Configuració de la Raspberry

Els passos a seguir requereixen disposar d'un Raspberry Pi amb RaspberryPi OS, una connexió Internet permanent i la possibilitat de connectar-se per Bluetooth.


| ⚠️ Atenció  | 
|------------|
| En el cas de no utilitzar una Raspberry o RaspberryPi OS, els passos a seguir poden canviar lleugerament. |


| 🛑 Atenció  |
|-------------|
| La xarxa XENA té un firewall bastant restrictiu, és recomanable portar l'equipament necessari (cable HDMI, adaptador per VGA, teclat, ...) per configurar el dispositiu in situ. |


### Instal·lació de les dependències

```bash
sudo apt update
sudo apt upgrade
sudo apt install python3-pip bluetooth pi-bluetooth bluez blueman libdbus-1-dev libdbus-glib-1-dev
```

### Sincronització amb els dispositius Bluetooth

Per poder extreure les dades dels sensors, és necessari sincronitzar-los abans. Anoteu el nom del dispositiu i la seva adreça MAC, seran de gran utilitat en un dels següents passos.

```bash
bluetoothctl
    power on
    scan on
    # Exemples de sensors :
    #   [NEW] Device E0:8D:E2:12:50:39 Aranet4 0E8AD
    #   [NEW] Device D2:C8:0F:F8:0F:CD Aranet4 03AA0
    scan off

    pair E0:8D:E2:12:50:39
    # Escriure els 6 números que surten a la pantalla del sensor
    disconnect

    pair D2:C8:0F:F8:0F:CD
    # Escriure els 6 números que surten a la pantalla del sensor
    disconnect
    
    quit
```

### Configuració de l'entorn

#### Descarregar el script

Creem la carpeta on guardarem el necessari.

```bash
mkdir ~/Desktop/aranet-python
cd ~/Desktop/aranet-python
```

Per continuar, és necessari passar els fitxers 'main.py' i 'requirements.txt' a la Raspberry Pi. Existeixen mil i una maneres per passar-los. La manera més fàcil (si s'està connectat per SSH) és de crear el fitxer amb 'nano' i copiar - pegar el contingut.


#### Requisits Python

Instal·lem les dependències del script a l'entorn virtual.

| ⚠️ Atenció  | 
|------------|
| Mentre s'instal·len els requisits de PIP, el pas "Building wheel for dbus-fast (pyproject.toml) ..." pot tardar més de 5 minuts... |

```bash
python -m venv ./venv

./venv/bin/pip3 install --upgrade pip setuptools wheel
./venv/bin/pip3 install -r ./requirements.txt
```

#### Variables d'entorn

És imprescindible d'assignar un identificador únic al dispositiu per tal de poder identificar-lo.

```bash
nano .env
```

```env
IDENTIFICADOR_RASPBERRY=IDENTIFICADOR UNIC
```

### Autentificació amb Google Cloud

Per l'autentificació amb Google Cloud s'utilitza el ADC (Application Default Credentials), més informació a [Google Cloud Docs](https://cloud.google.com/docs/authentication/provide-credentials-adc).

```bash
mkdir ~/.config/gcloud
nano ~/.config/gcloud/application_default_credentials.json
```


### Assignació de dispositius

Per tenir un registre dels dispositius instal·lats i dels sensors als quals es connecten, existeix una taula a la base de dades amb el nom 'atribucio_dispositius', que serveix per poder especificar de quins sensors recollirà dades. S'ha de completar el nom del dispositiu a configurar (el mateix que al fitxer '.env'), un identificador del sensor i la seva adreça MAC.

```sql
INSERT INTO `e3escoles.sensors.atribucio_dispositius`
VALUES ('ID_RASPBERRY', 'NOM SENSOR', 'ADRESSA MAC')
```

### Configurar el 'cronjob' per l'execució diaria

Per executar el programa cada dia, utilitzem 'cron'.

```bash
crontab -e
```

Configurem el PATH del programa a executar, ho fem cada dia a les 8 del matí (https://crontab.guru/)

```bash
0 8 * * * ~/Desktop/aranet-python/venv/bin/python3 ~/Desktop/aranet-python/main.py >> ~/Desktop/aranet-python/logs.txt
```

## Testos finals

### Comprovar una execució

Aquesta execució hauria de carregar tot l'històric disponible a la base de dades.

```bash
./venv/bin/python3 main.py
```

### Simular una execució diària

Aquesta seria l'execució del script diària, si tot va bé, és normal que el programa no faci cap print, ja que ho està guardant tot al fitxer 'logs.txt'

```bash
~/Desktop/aranet-python/venv/bin/python3 ~/Desktop/aranet-python/main.py >> ~/Desktop/aranet-python/logs.txt
cat logs.txt
```