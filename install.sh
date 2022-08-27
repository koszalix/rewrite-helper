#!/bin/bash

clone_repo(){
  git clone https://github.com/koszalix/rewrite-helper
  cd rewrite-helper || exit
}


install_python_dependency(){
  pip3 install loggin
  pip3 install request
  pip3 install icmplib
  pip3 install asyncio
}

prepare_directories(){
  mkdir /usr/share/rewrite-helper
  mkdir /usr/share/rewrite-helper/jobs
  mkdir /etc/rewrite-helper
  mkdir /var/log/rewrite-helper/
}

move_scripts(){
  cp -r src/*.py /usr/share/rewrite-helper/
  cp -r src/jobs/*.py /usr/share/rewrite-helper/jobs
  cp config.yml /etc/rewrite-helper/config.yml
}

create_links(){
  ln -s /usr/share/rewrite-helper/main.py /usr/bin/rewrite-helper
  sudo chmod +x /usr/bin/rewrite-helper
}

create_service(){
  cp rewrite-helper.service /etc/systemd/system/rewrite-helper.service
  systemctl enable rewrite-helper.service
}

if [ "$1" = "docker-build" ]
then
	clone_repo
	install_python_dependency
	prepare_directories
	move_scripts
	create_links
else	
	clone_repo
	install_python_dependency
	prepare_directories
	move_scripts
	create_links
	create_service
fi
