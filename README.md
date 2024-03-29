# Deluge Windscribe Container

Handles running a Deluge instance along side the Windscribe service.
If the Windscribe function is enabled, it is required to configure the
VPN itself. To simplify the process, config.ovpn files are used

The container will read the address and port details defined in the
config.ovpn to generate the required ufw firewall permissions.

## Supported Architectures
Images are build with the supported windscribe-cli architectures such as x86-64, and armhf. Docker manifest is being used for multi-platform awareness.
The architectures supported by this image are:

|Architecture|
|-----|
|x86-64|
|armhf|

## Getting Started

In order to run the container, you will need to create an auth.conf file with the username and password details. Then you can run the container command below it.

On first run, the deluge web UI will ask for a password. That password will be set to the default password, which is __deluge__.

### Environment Variables
You may use environment variables to configure your config files. The variables are as follows...

- VPN_USERNAME
- VPN_PASSWORD
- VPN_LOCATION
- WINDSCRIBE_FIREWALL
- LEGACY_IPTABLES

#### Synology Users and older Linux systems
If you run into the error message ```Error running "login"``` this is a sign that your iptables uses an older API call. Enable the environment variable ```LEGACY_IPTABLES=true``` to
force the system to use the legacy IPTables.

#### [Errno 1] Operation not permitted
If this error is thrown, that means that the OS is not allowing commands to execute in python. Currently the work around that has worked for me is setting the flag ```--privileged```. In the future, I'll take a closer look at which permissions are causing the problems.

### 1. Authorization
You will need to create a config file to auto-login to Windscribe.
You can either set some environment variables or configure a config file. The login information will be identical to the username and password you use to login to your windscribe profile. Below goes over both approaches.

#### Login Options
If VPN_USERNAME or VPN_PASSWORD is set, the /config/auth.conf will be ignored. Set the VPN settings to your Windscribe
login details. VPN_LOCATION is defaulted to _best_ and is optional.

#### /config/auth.conf file
A volume mount must be configured for this process to work. In the example shown below, we configure a folder to mount the current
working directory to $PWD/config:/config. The location of the config file will be the path set in the environment variable VPN_AUTH (/config/auth.conf). 
The file itself should contain three lines (no spaces).

```
<username>
<password>
<location|best>
```
The file will be automatically loaded when the container is started, otherwise the container will fail to connect and terminate. 

The location line is optional, but if defined will let you connect to a specific proxy location. For options, view the _Windscribe Location Options_ for options.

### 2. Container Command

To run the docker image, below is the typical configuration...

```cmd
docker run \
 -v $PWD/config:/config \
 -v $PWD/downloads:/downloads \
 -p 8112:8112 \
 -p 58846:58846 \
 --dns 8.8.8.8 \
 --cap-add=NET_ADMIN \
 --device /dev/net/tun:/dev/net/tun \
 --name deluge-windscribe \
 kabe0/deluge-windscribe
```

### Combining with other containers

If you want to combine this container with other docker containers in order to share the vpn connection you can chain the containers together using a service such as docker-compose. Below is an example of a docker-compose.yml file using both the deluge_windscribe container with sonarr. All the ports must be assigned to the main deluge-windscribe container.

```yml
version: "3"
services:
  deluge-windscribe:
    restart: unless-stopped
    image: kabe0/deluge-windscribe:latest
    volumes:
      - ./downloads:/downloads
      - ./config/deluge:/config
    dns:
      - 8.8.8.8
    ports:
      - 8112:8112
      - 8989:8989
      - 58846:58846
    cap_add:
      - NET_ADMIN
    devices:
      - /dev/net/tun
  sonarr:
    depends_on: [deluge-windscribe]
    restart: unless-stopped
    network_mode: "service:deluge-windscribe"
    image: linuxserver/sonarr:latest
    volumes:
      - ./config/sonarr:/config
      - ./downloads:/downloads
```

### Command Details
The --device is required to ensure that the Windscribe can set the necessary configuration details.
The default option should always be /dev/net/tun.
 
--cap-add=NET_ADMIN is also needed to ensure that
the Windscribe service has enough permissions to change the network configuration for the docker container.

### Volumes

| Docker Path | Description |
| -------| ----------- |
| /config | The main config directory for deluge and the docker container home directory.|
| /downloads | The folder where files are downloaded to. |

### Environment Variables

| Name | Default | Description |
| ---- | ------- | ----------- |
| WEB_PORT | 8112 | The port used by the deluge-web for displaying the html content. |
| DEL_PORT | 58846 | The port the Daemon runs on. |
| DEL_UID | 1000 | The ID used for the main deluge user account. Changing this value could break the config folder. |
| DEL_GID | 1000 | The ID used for the main deluge group account. Changing this value could break the config folder. |
| VPN_ENABLE | True | Disables the VPN if needed for debugging
| VPN_AUTH | /config/auth.conf | The path for the auth.conf which should store the username and password. If the file is not found, the application will still try to connect to the Windscribe server. |
| VPN_USERNAME | null | (Optional) alternative to using the VPN_AUTH file. VPN_PASSWORD must also be set at the same time.
| VPN_PASSWORD | null | (Optional) alternative to using the VPN_AUTH file. VPN_USERNAME must also be set at the same time.
| VPN_LOCATION | best | (Optional) alternative to using the VPN_AUTH file.
| HOME | /config | The path to the home directory.|
| WINDSCRIBE_FIREWALL | on | Toggle the firewall mode for Windscribe
| LEGACY_IPTABLES | False | Can be turned on to setup legacy tables if the base OS uses the legacy iptables protocol.

#### (Optional) WINDSCRIBE_FIREWALL Variable Details
This variable has three possible values:
- **on**:     Always active regardless connection status.
- _auto_:   Only active when we are connected.
- _off_:    Windscribe firewall is deactivated.

#### (Optional) Webproxy Configuration
If WEBPROXY_ENABLED is true, then a web-proxy server to allow you to tunnel your web-browser traffic through the same VPN connection is started. 

The default listening port is 8888. Note that only ports above 1024 can be specified as all ports below 1024 are privileged and would otherwise require root permissions to run. Remember to add a port binding for your selected (or default) port when starting the container. If you set Username and Password it will enable BasicAuth for the proxy.:

- WEBPROXY_PORT
- WEBPROXY_USERNAME
- WEBPROXY_PASSWORD
- PROXY_CONF

### Windscribe Location Options
You may use any of the values to select a location. The Label column allows connecting directly to a single VPN location.

| Location | Short Name | City Name | Label |
| -------- | ---------- | --------- | ----- |
|US Central|US-C|Atlanta|Mountain|
|US Central|US-C|Atlanta|Piedmont|
|US Central|US-C|Dallas|Ammo|
|US Central|US-C|Dallas|BBQ|
|US Central|US-C|Dallas|Ranch|
|US Central|US-C|Denver|Hops|
|US Central|US-C|Salt Lake City|Cottonwood|
|US East|US|Boston|MIT|
|US East|US|Buffalo|Bill|
|US East|US|Charlotte|Earnhardt|
|US East|US|Chicago|Cub|
|US East|US|Chicago|The L|
|US East|US|Chicago|Wrigley|
|US East|US|Miami|Florida Man|
|US East|US|Miami|Snow|
|US East|US|Miami|Vice|
|US East|US|New Jersey|Situation|
|US East|US|New York|Empire|
|US East|US|New York|Gotham|
|US East|US|New York|Insomnia|
|US East|US|Orlando|Tofu Driver|
|US East|US|Washington DC|Precedent|
|US West|US-W|Bend|Oregon Trail|
|US West|US-W|Las Vegas|Casino|
|US West|US-W|Los Angeles|Cube|
|US West|US-W|Los Angeles|Dogg|
|US West|US-W|Los Angeles|Eazy|
|US West|US-W|Los Angeles|Lamar|
|US West|US-W|Los Angeles|Pac|
|US West|US-W|Phoenix|Floatie|
|US West|US-W|San Francisco|Sanitation|
|US West|US-W|San Jose|Santana|
|US West|US-W|Santa Clara|Inside|
|US West|US-W|Seattle|Cobain|
|US West|US-W|Seattle|Cornell|
|US West|US-W|Seattle|Hendrix|
|WINDFLIX US|US-N|New York|Radiohall|
|Canada East|CA|Halifax|Howe|
|Canada East|CA|Montreal|Bagel Poutine|
|Canada East|CA|Montreal|Old Port|
|Canada East|CA|Toronto|Comfort Zone|
|Canada East|CA|Toronto|The 6|
|Canada West|CA-W|Vancouver|Granville|
|Canada West|CA-W|Vancouver|Vansterdam|
|WINDFLIX CA|CA-N|Toronto|Mansbridge|
|Austria|AT|Vienna|Boltzmann|
|Austria|AT|Vienna|Hofburg|
|Belgium|BE|Brussels|Guildhouse|
|Bulgaria|BG|Sofia|Nevski|
|Croatia|HR|Zagreb|Tkalciceva|
|Cyprus|CY|Nicosia|Blue Lagoon|
|Czech Republic|CZ|Prague|Vltava|
|Czech Republic|CZ|Prague|Staromak|
|Denmark|DK|Copenhagen|Rosenborg|
|Denmark|DK|Copenhagen|Tivoli|
|Estonia|EE|Tallinn|Kiek in de Kok|
|Estonia|EE|Tallinn|Lennujaam|
|Finland|FI|Helsinki|Suomenlinna|
|Finland|FI|Helsinki|Tram|
|France|FR|Paris|Jardin|
|France|FR|Paris|Seine|
|Germany|DE|Frankfurt|Castle|
|Germany|DE|Frankfurt|Wiener|
|Greece|GR|Athens|Agora|
|Greece|GR|Athens|Odeon|
|Greece|GR|Athens|Parthenon|
|Hungary|HU|Budapest|Danube|
|Iceland|IS|Reykjavik|Fuzzy Pony|
|Ireland|IE|Dublin|Guinness|
|Israel|IL|Ashdod|Yam Park|
|Israel|IL|Jerusalem|Zion|
|Italy|IT|Milan|Duomo|
|Italy|IT|Milan|Galleria|
|Italy|IT|Rome|Colosseum|
|Latvia|LV|Riga|Daugava|
|Lithuania|LT|Siauliai|Talksa|
|Macedonia|MK|Skopje|Vardar|
|Moldova|MD|Chisinau|Dendrarium|
|Netherlands|NL|Amsterdam|Bicycle|
|Netherlands|NL|Amsterdam|Canal|
|Netherlands|NL|Amsterdam|Red Light|
|Netherlands|NL|Amsterdam|Tulip|
|Norway|NO|Oslo|Fjord|
|Poland|PL|Warsaw|Chopin|
|Poland|PL|Warsaw|Curie|
|Poland|PL|Warsaw|Vistula|
|Portugal|PT|Lisbon|Bairro|
|Romania|RO|Bucharest|No Vampires|
|Slovakia|SK|Bratislava|Devin Castle|
|Spain|ES|Barcelona|Batllo|
|Spain|ES|Madrid|Prado|
|Sweden|SE|Stockholm|Djurgarden|
|Sweden|SE|Stockholm|Old Town|
|Sweden|SE|Stockholm|Syndrome|
|Switzerland|CH|Zurich|Alphorn|
|Switzerland|CH|Zurich|Altstadt|
|Switzerland|CH|Zurich|Lindenhof|
|Tunisia|TN|Tunis|Medina|
|United Kingdom|GB|London|Biscuits|
|United Kingdom|GB|London|Crumpets|
|United Kingdom|GB|London|Custard|
|United Kingdom|GB|Manchester|United|
|WINDFLIX UK|GB-N|London|The Tube|
|Albania|AL|Tirana|Besa|
|Azerbaijan|AZ|Baku City|Caspian|
|Bosnia|BA|Sarajevo|Burek|
|India|IN|Chennai|Adyar|
|India|IN|Indore|Sarafa|
|Russia|RU|Moscow|The Putin|
|Russia|RU|Saint Petersburg|Hermitage|
|Russia|RU|Saint Petersburg|Peterhof|
|Serbia|RS|Belgrade|Rakia|
|Slovenia|SI|Ljubljana|Melania|
|Slovenia|SI|Ljubljana|Tromostovje|
|South Africa|ZA|Johannesburg|District|
|South Africa|ZA|Johannesburg|Ellis Park|
|South Africa|ZA|Johannesburg|Lindfield|
|Turkey|TR|Bursa|Teleferik|
|Turkey|TR|Istanbul|Ataturk|
|Turkey|TR|Istanbul|Galata|
|Ukraine|UA|Kyiv|Horilka|
|Australia|AU|Adelaide|Oval|
|Australia|AU|Brisbane|Bad Koala|
|Australia|AU|Melbourne|Yarra|
|Australia|AU|Perth|Kings Park|
|Australia|AU|Sydney|Opera House|
|New Zealand|NZ|Auckland|Parnell|
|Hong Kong|HK|Hong Kong|Phooey|
|Hong Kong|HK|Hong Kong|Victoria|
|Indonesia|ID|Jakarta|Menteng|
|Indonesia|ID|Jakarta|Senayan|
|Japan|JP|Tokyo|Bosozoku|
|Japan|JP|Tokyo|Drift|
|Japan|JP|Tokyo|Sake|
|Malaysia|MY|Kuala Lumpur|Perdana|
|Philippines|PH|San Antonio|Zambales|
|Singapore|SG|Singapore|Garden|
|Singapore|SG|Singapore|Marina Bay|
|Singapore|SG|Singapore|SMRT|
|South Korea|KR|Seoul|Bukhansan|
|South Korea|KR|Seoul|Metro|
|Taiwan|TW|Taipei|Datong|
|Thailand|TH|Bangkok|Khao San|
|Thailand|TH|Bangkok|Reclining Buddha|
|United Arab Emirates  AE|Dubai|Khalifa
|Vietnam|VN|Hanoi Red River|
|WINDFLIX JP|JP-N|Tokyo|Kaiju|
|Argentina|AR|Buenos Aires|Madero|
|Argentina|AR|Buenos Aires|Tango|
|Brazil|BR|Sao Paulo|Mercadao|
|Brazil|BR|Sao Paulo|Pinacoteca|
|Colombia|CO|Bogota|White Coffee|
|Mexico|MX|Guadalajara|Cabanas|
|Fake Antarctica|AQ|Troll Station|- |
