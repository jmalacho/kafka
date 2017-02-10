FROM jmalacho/base
MAINTAINER Jon Malachowski "jmalacho@gmail.com"

#RUN git clone --depth 1 https://github.com/jmalacho/kafka.git /ansible && \
RUN git clone --depth 1 https://github.com/jmalacho/kafka.git /ansible && \
    ansible-playbook -v /ansible/install.yml && \
    rm -rf /ansible
    

EXPOSE 2181 9092

CMD /docker-cmd
