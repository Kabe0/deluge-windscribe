FROM ubuntu:18.04

LABEL maintainer="kabe0"

# environment settings
ARG DEBIAN_FRONTEND="noninteractive"
ENV HOME="/config"

ENV WEB_PORT=8112
ENV DEL_PORT=58846
ENV DEL_UID=1000
ENV DEL_GID=1000

ENV VPN_ENABLE=True
ENV VPN_AUTH="/config/auth.conf"
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1

# add repo and install qbitorrent
RUN \
 apt-get update && \
 apt-get install -y \
 software-properties-common dirmngr gpg-agent && \
 apt-key adv --no-tty --keyserver keyserver.ubuntu.com --recv-key FDC247B7 && \
 echo 'deb https://repo.windscribe.com/ubuntu zesty main' | tee /etc/apt/sources.list.d/windscribe-repo.list && \
 LC_ALL=C.UTF-8 add-apt-repository ppa:deluge-team/stable && \
 apt-get update && \
 apt-get install -y \
	python3 python3-pip windscribe-cli iptables-persistent deluged deluge-web deluge-console resolvconf- && \
	# Dev tools nano dnsutils iputils-ping lsof
 python3 -m pip install pexpect && \
 apt-get clean && \
 rm -rf \
  /tmp/* \
  /var/lib/apt/lists/* \
  /var/tmp/* && \
 apt-get autoremove && \
 apt-get clean && \
 apt-get purge -y \
    software-properties-common dirmngr gpg-agent && \
 useradd -m -d $HOME deluge

# ports and volumes
EXPOSE 8112 6881/udp
VOLUME /config /downloads
COPY init.py run.py run.sh /usr/bin/

CMD /usr/bin/python3 /usr/bin/init.py
