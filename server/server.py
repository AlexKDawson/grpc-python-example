import grpc
import logging
from concurrent import futures
from google.protobuf import wrappers_pb2
from protos import read_text_file_pb2_grpc

class MyFileReader(read_text_file_pb2_grpc.FileReaderServicer):

  # Checks name and pin credentials returns contents of secret.txt
  # if credentials are valid, returns None if not.
  def read_secret_file(self, request, context):
    logging.debug("Received call to read secret file")

    retValue = None

    if request.name == "Alex" and request.pin == 1234:
      logging.debug("Access Granted")
      with open("res/secret.txt", "r") as file:
        retValue = wrappers_pb2.StringValue(value = file.read())
    else:
      logging.debug("Access Denied")

    return retValue

def serve():
  with futures.ThreadPoolExecutor(max_workers=10) as executor:
    server = grpc.server(executor)
    read_text_file_pb2_grpc.add_FileReaderServicer_to_server(MyFileReader(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.debug("Server Started")
    server.wait_for_termination()

if __name__ == '__main__':
  logging.basicConfig(level = logging.NOTSET)
  serve()