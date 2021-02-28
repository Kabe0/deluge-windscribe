FROM debian:bullseye-slim

LABEL maintainer="kabe0"

# environment settings
ARG DEBIAN_FRONTEND="noninteractive"
ENV HOME="/config"

ENV WEB_PORT=8112
ENV DEL_PORT=58846
ENV DEL_UID=1000
ENV DEL_GID=1000
ENV DEL_INT=tun0

ENV VPN_ENABLE=True
ENV VPN_AUTH="/config/auth.conf"
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
ENV WEBPROXY_ENABLED=true
ENV WEBPROXY_PORT=8888
ENV WEBPROXY_USERNAME=
ENV WEBPROXY_PASSWORD=
ENV WINDSCRIBE_FIREWALL="auto"

RUN \
 apt-get update && \
 apt-get install -y  && \
 apt-get install -y software-properties-common dirmngr apt-transport-https && \
 apt-key adv --no-tty --keyserver keyserver.ubuntu.com --recv-key FDC247B7 && \
 echo 'deb https://repo.windscribe.com/debian buster main' | tee /etc/apt/sources.list.d/windscribe-repo.list && \
 apt-get update && \
 apt-get install -y \
	python3 python3-pip windscribe-cli iptables-persistent deluged deluge-web deluge-console resolvconf- \
	nano dnsutils iputils-ping lsof net-tools cron && \
 python3 -m pip install pexpect netifaces netaddr pyufw psutil && \
 echo "**** Install tinyproxy ****" && \
 apt-get install -y \
   tinyproxy && \
 apt-get clean && \
 rm -rf \
  /tmp/* \
  /var/lib/apt/lists/* \
  /var/tmp/* && \
 apt-get autoremove && \
 apt-get clean && \
 apt-get purge -y \
    software-properties-common dirmngr gpg-agent && \
 useradd -m -d $HOME deluge && \
 usermod -a -G users deluge

ADD tinyproxy /opt/tinyproxy/

EXPOSE 8112 6881/udp
VOLUME /config /downloads
COPY init.py run.py run.sh up.py unblock.sh lifeline.sh /usr/bin/
COPY core.conf /usr/local/etc/
COPY unblock-cron /etc/cron.d/unblock-cron

RUN crontab /etc/cron.d/unblock-cron

CMD ["/usr/bin/lifeline.sh"]
