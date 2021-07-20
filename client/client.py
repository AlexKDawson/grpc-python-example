import grpc
from protos import read_text_file_pb2_grpc
from protos import read_text_file_pb2

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = read_text_file_pb2_grpc.FileReaderStub(channel)
    response = stub.read_secret_file(read_text_file_pb2.read_secret_request(name="Alex", pin=1234))
    print(response.value)

if __name__ == '__main__':
  run()