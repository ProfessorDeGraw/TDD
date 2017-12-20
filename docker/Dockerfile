from ubuntu

RUN apt-get update
RUN apt-get dist-upgrade -y

RUN DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python-software-properties
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install software-properties-common
RUN DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:jonathonf/python-3.6;
RUN apt-get update
RUN apt-get -y install --no-install-recommends apt-utils;
RUN apt-get -y upgrade;
RUN apt-get -y install bash;
RUN apt-get -y install vim;
RUN apt-get -y install git;
RUN apt-get -y install openssh-client;
RUN apt-get -y install openssh-server;
RUN apt-get -y install nginx;
RUN apt-get -y install netcat;
RUN apt-get -y install iceweasel;
RUN apt-get -y install libgconf-2-4; 
RUN apt-get -y install imagemagick;
RUN apt-get -y install tcpdump; 
RUN apt-get -y install net-tools; 
RUN apt-get -y install xvfb; 
RUN apt-get -y install python3; 
RUN apt-get -y install python3.6;
RUN apt-get -y install python-pip;

RUN mkdir /var/run/sshd
RUN echo 'root:screencast' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

ENV SITENAME tdd-staging

EXPOSE 22

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN echo "server {" >> /etc/nginx/sites-available/$SITENAME
RUN echo "    listen 80;" >> /etc/nginx/sites-available/$SITENAME
RUN echo "    server_name "$SITENAME";" >> /etc/nginx/sites-available/$SITENAME
RUN echo "" >> /etc/nginx/sites-available/$SITENAME
RUN echo "    location / {" >> /etc/nginx/sites-available/$SITENAME
RUN echo "        proxy_pass http://localhost:8000;" >> /etc/nginx/sites-available/$SITENAME
RUN echo "    }" >> /etc/nginx/sites-available/$SITENAME
RUN echo "}" >> /etc/nginx/sites-available/$SITENAME
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/$SITENAME /etc/nginx/sites-enabled/$SITENAME

EXPOSE 80

RUN mkdir -p /sites/$SITENAME/database
RUN mkdir -p /sites/$SITENAME/static
RUN git clone https://github.com/ProfessorDeGraw/TDD.git /sites/$SITENAME/source

EXPOSE 8000

RUN pip install virtualenvwrapper;

RUN /bin/bash -c ' \
    export WORKON_HOME=/sites/$SITENAME/virtualenv; \
    source /usr/local/bin/virtualenvwrapper.sh; \
    pip install virtualenv; \
    mkvirtualenv -p python3.6 tdd36; \
    pip install virtualenv; \
    pip install Django; \
    '

RUN touch services.sh
RUN chmod +x services.sh
RUN echo "exec /usr/sbin/sshd -D &" >> services.sh
RUN echo "nginx &" >> services.sh
RUN echo "cd /sites/$SITENAME/source" >> services.sh
RUN echo "/sites/$SITENAME/virtualenv/tdd36/bin/pip install -r requirements.txt" >> services.sh
RUN echo "/sites/$SITENAME/virtualenv/tdd36/bin/python manage.py runserver" >> services.sh

CMD ["sh", "./services.sh"]
