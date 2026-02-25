from redis import Redis
from rq import Queue, SimpleWorker

redis_conn = Redis(host = "localhost", port = 6379, db = 0)
queue = Queue("financial_queue", connection = redis_conn)

if __name__ == "__main__":
    worker = SimpleWorker([queue], connection = redis_conn)
    print("Starting SimpleWorker....")
    worker.work()
    