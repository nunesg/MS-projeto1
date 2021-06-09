class ClientSummary:
  def __init__(self, data):
    self.id = data['id']
    self.rel_arrival_time = data['rel_arrival_time']
    self.arrival_time = data['arrival_time']
    self.service_time = data['service_time']
    self.start_service_time = data['start_service_time']
    self.finish_service_time = data['finish_service_time']
    self.queue_time = data['queue_time']
    self.system_time = data['system_time']
    self.server_id = data['server_id']
    self.idle_time = data['idle_time']

  def keys(self):
    return [
      "ID", 
      "rel_arrival_time", 
      "arrival_time", 
      "service_time", 
      "start_service_time", 
      "finish_service_time", 
      "queue_time", 
      "system_time", 
      "server_ID", 
      "idle_time"
    ]
  
  def values(self):
    return [
      self.id, 
      self.rel_arrival_time, 
      self.arrival_time, 
      self.service_time, 
      self.start_service_time, 
      self.finish_service_time, 
      self.queue_time, 
      self.system_time, 
      self.server_id, 
      self.idle_time,
    ]

class DroppedClientSummary:
  def __init__(self, data):
    self.id = data['id']
    self.arrival_time = data['arrival_time']

  def keys(self):
    return ["ID", "arrival_time"]
  
  def values(self):
    return [self.id, self.arrival_time]