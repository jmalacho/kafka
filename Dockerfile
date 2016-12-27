FROM jmalacho/base
MAINTAINER Jon Malachowski "jmalacho@gmail.com"

RUN git clone https://github.com/jmalacho/kafka.git /ansible
RUN ansible-playbook -v /ansible/ansible.yml
