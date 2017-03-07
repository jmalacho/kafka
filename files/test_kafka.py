from confluent_kafka import Consumer, KafkaException, KafkaError
from confluent_kafka import Producer
from time import time as now
import socket
import sys

# https://github.com/confluentinc/confluent-kafka-python/tree/master/examples

class TimeoutException(Exception):
    pass

def timeoutCheck( timeout=-1 ):
  if timeout > 0:
    timeoutCheck.t=now() + timeout
  if timeoutCheck.t - now() < 0:
    raise TimeoutException
  else:
    print "timeoutCheck OK"

def wait_net_service(server, port, timeout=None):
    """ Wait for network service to appear 
        @param timeout: in seconds, if None or 0 wait forever
        @return: True of False, if timeout is None may return only True or
                 throw unhandled network exception
    """
    import socket
    import errno
    import time

    s = socket.socket()
    if timeout:
        # time module is needed to calc timeout shared between two exceptions
        end = now() + timeout

    while True:
        try:
            if timeout:
                next_timeout = end - now()
                if next_timeout < 0:
                    return False
                else:
                    s.settimeout(next_timeout)

            s.connect((server, port))

        except socket.timeout, err:
            # this exception occurs only if timeout is set
            if timeout:
                return False

        except socket.error, err:
            # catch timeout exception from underlying network library
            # this one is different from socket.timeout
            if type(err.args) != tuple:
                raise
            else:
                print err
            # or err[0] != errno.ETIMEDOUT:
        else:
            s.close()
            return True
        time.sleep(1)

def test_service(zookeeper="kafka", kafka="kafka"): 
   assert wait_net_service( zookeeper, 2181, 30) 
   assert wait_net_service( "kafka", 9092, 30) 

def test_zookeeper(zookeeper="kafka"):
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
   server_address = (zookeeper, 2181)
   message="ruok"
   try:
     sock.connect(server_address)
     sock.sendall(message)
     r=sock.recv(1024)
     assert (r=="imok")
   finally:
     sock.close() 

def test_send(topic="testtopic", message="Example message"):
   conf={'bootstrap.servers': 'kafka'}
   p = Producer(**conf)
   p.produce(topic, message)
   p.poll(0)
   p.flush()
   assert True

def assignment(consumer, partitions):
   print('Assignment:', partitions)
   assignment.isAssigned=True


import random
def test_consume():
   group="testConsume%d" % round( random.uniform(1, 9999 ) )
   topic="testConsumeTopic%d" % round( random.uniform(1, 9999 ) )
   conf={'bootstrap.servers': 'kafka', 'group.id': group,
         'default.topic.config': {'auto.offset.reset': 'latest'},
         'api.version.request': "true"
        }
   #'default.topic.config': {'auto.offset.reset': 'earliest'}
   #'default.topic.config': {'auto.offset.reset': 'latest'},
   c = Consumer(**conf)
   assignment.isAssigned=False
   c.subscribe( [ topic ], assignment )
   while not assignment.isAssigned:
      print "Waiting for Subscription"
      c.poll( timeout=1.0 )

   print "About to send message"
   test_send(topic, "Example message 1" )

   running=True
   timeoutCheck(4)
   while running:
     timeoutCheck()
     msg = c.poll( timeout=1.0 )
     if msg is None:
         print "No message received"
         continue
     if not msg.error():
         print('(%s) Receiving message: %s' % (1, msg.value().decode('utf-8')) )
         running = False
     elif msg.error().code() != KafkaError._PARTITION_EOF:
         assert False, msg.error()
   c.close()


