from ubuntu

RUN apt-get update; \
    apt-get dist-upgrade -y; \
    DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade ; \
    DEBIAN_FRONTEND=noninteractive apt-get -y install python-software-properties; \
    DEBIAN_FRONTEND=noninteractive apt-get -y install software-properties-common; \
    DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:jonathonf/python-3.6; \
    apt-get update; \
    apt-get -y install --no-install-recommends apt-utils; \
    apt-get -y upgrade; \
    apt-get -y install bash; \
    apt-get -y install vim; \
    apt-get -y install git; \
    apt-get -y install openssh-client; \
    apt-get -y install openssh-server; \
    apt-get -y install nginx; \
    apt-get -y install netcat; \
    apt-get -y install iceweasel; \
    apt-get -y install libgconf-2-4; \
    apt-get -y install imagemagick; \
    apt-get -y install tcpdump; \
    apt-get -y install net-tools; \
    apt-get -y install xvfb; \
    apt-get -y install python3; \
    apt-get -y install python3.6; \
    apt-get -y install python-pip;

RUN mkdir /var/run/sshd; \
    echo 'root:screencast' | chpasswd; \
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config; \
    sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

ENV SITENAME tdd-staging

EXPOSE 22

RUN echo "daemon off;" >> /etc/nginx/nginx.conf ; \
    echo "server {" 				>> /etc/nginx/sites-available/$SITENAME; \
    echo "    listen 80;" 			>> /etc/nginx/sites-available/$SITENAME; \
    echo "    server_name "$SITENAME";" 	>> /etc/nginx/sites-available/$SITENAME; \
    echo "" 					>> /etc/nginx/sites-available/$SITENAME; \
    echo "    location /static {" 		>> /etc/nginx/sites-available/$SITENAME; \
    echo "        alias /sites/"$SITENAME"/static;" \
						>> /etc/nginx/sites-available/$SITENAME; \
    echo "    }" 				>> /etc/nginx/sites-available/$SITENAME; \
    echo "" 					>> /etc/nginx/sites-available/$SITENAME; \
    echo "    location / {" 			>> /etc/nginx/sites-available/$SITENAME; \
    echo "        proxy_set_header Host \$host;" >> /etc/nginx/sites-available/$SITENAME; \
    echo "        proxy_pass http://unix:/tmp/"$SITENAME".socket;" \
						>> /etc/nginx/sites-available/$SITENAME; \
    echo "    }" 				>> /etc/nginx/sites-available/$SITENAME; \
    echo "}" 					>> /etc/nginx/sites-available/$SITENAME; \
    rm /etc/nginx/sites-enabled/default; \
    ln -s /etc/nginx/sites-available/$SITENAME /etc/nginx/sites-enabled/$SITENAME;

EXPOSE 80
EXPOSE 8000

RUN mkdir -p /sites/$SITENAME/database; \
    mkdir -p /sites/$SITENAME/static; \
    pip install virtualenvwrapper; \
    /bin/bash -c ' \
    export WORKON_HOME=/sites/$SITENAME/virtualenv; \
    source /usr/local/bin/virtualenvwrapper.sh; \
    pip install virtualenv; \
    mkvirtualenv -p python3.6 tdd36; \
    pip install virtualenv; \
    pip install Django; \
    pip install gunicorn; \
    '; \
    touch services.sh; \
    chmod +x services.sh; \
    echo "exec /usr/sbin/sshd -D &" >> services.sh; \
    echo "nginx &" >> services.sh; \
    echo "cd /sites/$SITENAME/source" >> services.sh; \
    echo "/sites/$SITENAME/virtualenv/tdd36/bin/pip install -r requirements.txt" >> services.sh; \
    echo "/sites/$SITENAME/virtualenv/tdd36/bin/python manage.py migrate --noinput" >> services.sh; \
    echo "/sites/$SITENAME/virtualenv/tdd36/bin/python manage.py collectstatic --noinput" >> services.sh; \
    echo "/sites/$SITENAME/virtualenv/tdd36/bin/gunicorn " \
		"--bind unix:/tmp/"$SITENAME".socket" \ 
                "tdd.wsgi:application" >> services.sh;

#    echo "/sites/$SITENAME/virtualenv/tdd36/bin/python manage.py runserver" >> services.sh; 

ADD https://api.github.com/repos/ProfessorDeGraw/TDD/git/refs/heads/master version.json
RUN git clone https://github.com/ProfessorDeGraw/TDD.git /sites/$SITENAME/source

CMD ["sh", "./services.sh"]
