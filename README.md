# Deluge Windscribe Container

Handles running a Deluge instance along side the Windscribe service.
If the Windscribe function is enabled, it is required to configure the
VPN itself. To simplify the process, config.ovpn files are used

The container will read the address and port details defined in the
config.ovpn to generate the required ufw firewall permissions.

## Getting Started

To run the docker image, below is the typical configuration...

```cmd
docker run \
 -v $PWD/config:/config \
 -v $PWD/downloads:/downloads \
 -p 8112:8112 \
 --cap-add=NET_ADMIN \
 --device /dev/net/tun:/dev/net/tun \
 --name deluge-windscribe \
 kabe0/deluge-windscribe
```

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
| VPN_AUTH | /config/auth.conf | The path for the auth.conf which should store the username and password. If the file is not found, the application will still try to connect to the Windscribe server. |
| HOME | /config | The path to the home directory.|
