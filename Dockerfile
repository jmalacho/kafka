FROM jmalacho/base
MAINTAINER Jon Malachowski "jmalacho@gmail.com"

RUN git clone https://github.com/jmalacho/kafka.git /ansible
RUN ansible-playbook -v /ansible/install.yml

EXPOSE 2181 9092

CMD ansible-playbook -v /ansible/start.yml
