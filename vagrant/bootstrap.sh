#!/usr/bin/env bash

SRC="/usr/local/src"
GIT="git-1.9.2"
MYSQL_DIR=$SRC/mysql
ES_DIR=$SRC/elasticsearch
ES_PLUGIN=/usr/share/elasticsearch/bin/plugin

# basic
sudo apt-get update
sudo mkdir -p $SRC
sudo apt-get -y install make curl lv
sudo groupadd t-atsumi
sudo useradd -m -d /home/t-atsumi -s /bin/bash -g t-atsumi t-atsumi
sudo update-locale LANG=ja_JP.UTF-8


# git
sudo apt-get -y install libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev build-essential
cd $SRC
sudo wget https://www.kernel.org/pub/software/scm/git/${GIT}.tar.gz
sudo tar xzf ${GIT}.tar.gz
cd $GIT
sudo ./configure
sudo make
sudo make install


# mysql
sudo apt-get -y install libaio1

sudo mkdir -p ${MYSQL_DIR}
cd ${MYSQL_DIR}
sudo wget http://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.17-debian6.0-x86_64.deb
sudo dpkg -i mysql-5.6.17-debian6.0-x86_64.deb

sudo cp -p my.cnf /etc/my.cnf
sudo chown root:root /etc/my.cnf

sudo mkdir /var/log/mysql
sudo groupadd mysql
sudo useradd -r -g mysql mysql
sudo chown -R root:root /opt/mysql
sudo chown -R mysql:mysql /opt/mysql/server-5.6
sudo chown -R mysql:mysql /var/log/mysql

sudo install -o mysql -g mysql -d /data/mysql
sudo -u mysql /opt/mysql/server-5.6/scripts/mysql_install_db --user=mysql --datadir=/data/mysql
sudo cp /opt/mysql/server-5.6/support-files/mysql.server /etc/init.d/mysql
sudo update-rc.d mysql defaults
sudo cat <<EOF > /etc/profile.d/mysql.sh
PATH="/opt/mysql/server-5.6/bin:${PATH}"
MANPATH="/opt/mysql/server-5.6/man:${MANPATH}"
EOF
sudo chmod 755 /etc/profile.d/mysql.sh


# redis
cd $SRC
sudo wget http://download.redis.io/releases/redis-2.8.9.tar.gz
sudo tar xzf redis-2.8.9.tar.gz
cd redis-2.8.9
sudo make
sudo make install
sudo mkdir /etc/redis
sudo mkdir -p /var/redis/6379
sudo cp utils/redis_init_script /etc/init.d/redis_6379
sudo cp redis.conf /etc/redis/6379.conf
sudo update-rc.d redis_6379 defaults


# python3.4
cd $SRC
sudo wget https://www.python.org/ftp/python/3.4.0/Python-3.4.0.tar.xz
sudo tar Jxf Python-3.4.0.tar.xz
cd Python-3.4.0
sudo ./configure
sudo make
sudo make install

python3.4 -m ensurepip
sudo pip3 install virtualenv
sudo pip3 install flake8
sudo pip3 install ipython

cd $SRC
sudo apt-get -y install libmysqlclient-dev
sudo wget https://github.com/PyMySQL/mysqlclient-python/archive/1.3.0.tar.gz -O mysqlclient-python-1.3.0.tar.gz
sudo pip3 install $SRC/mysqlclient-python-1.3.0.tar.gz


# elasticsearch
sudo apt-get -y install openjdk-7-jdk
sudo mkdir -p $ES_DIR
cd $ES_DIR
sudo wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.1.1.deb
sudo dpkg -i elasticsearch-1.1.1.deb

sudo $ES_PLUGIN -install elasticsearch/marvel/latest
sudo $ES_PLUGIN -install polyfractal/elasticsearch-inquisitor
sudo $ES_PLUGIN -install elasticsearch/elasticsearch-analysis-kuromoji/2.1.0
sudo $ES_PLUGIN -install royrusso/elasticsearch-HQ

sudo rm -rf /etc/mysql

# for virtual
sudo ufw disable
