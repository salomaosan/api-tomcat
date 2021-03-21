"""
Formas de buscar os dados.
  localhost:5000/host/port/key_zabbix ex: -> jmx["java.lang:type=Memory","HeapMemoryUsage.used"]' 192.168.9.111 3080
  localhost:5000/host/port/key_zabbix ex: -> jmx.get[attributes,"java.nio:name=direct,type=BufferPool"]' 192.168.9.111 3080
  localhost:5000/host/port/key_zabbix ex: -> jmx.discovery[attributes,"java.lang:type=Memory"]' 192.168.9.111 3080

"""

import json, socket, os, re

def get_dados(jmx_server, jmx_port, jmx_key, java_gateway_host = '127.0.0.1', java_gateway_port = 10052):
  query = {'request': 'java gateway jmx',
          'conn': jmx_server, 'port': jmx_port,
          'keys': [jmx_key] }
  # Original jmx_endpoint
  query['jmx_endpoint'] = 'service:jmx:rmi:///jndi/rmi://%s:%s/jmxrmi' % (jmx_server, jmx_port)
  # query['jmx_endpoint'] = 'service:jmx:remote://%s:%s/' % (conn, port)

  query_str = json.dumps(query)
  query_len = len(query_str)
  query_len_hex = '%.16x' % query_len
  query_len_bin = re.sub(r'^(..)(..)(..)(..)(..)(..)(..)(..)', '\\x\\8\\x\\7\\x\\6\\x\\5\\x\\4\\x\\3\\x\\2\\x\\1', query_len_hex)
  query_bin = "ZBXD\\x01%s" % (query_len_bin)
  query_bin = query_bin.encode('latin-1').decode('unicode_escape')
  query_bin += query_str

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((java_gateway_host,java_gateway_port))
    s.send(bytes(query_bin, 'latin-1'))
    size = 1024
    data = s.recv(size)
    full = ''
    started = False
    while len(data):
      data = str(data, 'latin-1')
      if not started:
        if '{' in data:
          data = data[data.index('{'):]
          started = True
        else:
          data = ''
      if started:
        full += data
      data = s.recv(size)
    
    full = parse_to_json(full)
    return(full)

def parse_to_json(data_string):
  json_parse = json.loads(data_string)
  remove_data = json_parse["data"]
  remove_list = remove_data[0]
  final_data = remove_list["value"]
  return(json.loads(final_data))
  