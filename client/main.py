import json

import src.pb.tfidf.v1.service_pb2 as service_pb2
import src.pb.tfidf.v1.service_pb2_grpc as service_pb2_grpc
import grpc

channel = grpc.insecure_channel("localhost:50051")
stub = service_pb2_grpc.MovieGenreStub(channel)
res = stub.Predict(
    service_pb2.PredictRequest(
        synopsis="""
When their kingdom becomes trapped in perpetual winter, fearless Anna (Kristen Bell) joins forces with mountaineer Kristoff (Jonathan Groff) and his reindeer sidekick to find Anna's sister, Snow Queen Elsa (Idina Menzel), and break her icy spell. Although their epic journey leads them to encounters with mystical trolls, a comedic snowman (Josh Gad), harsh conditions, and magic at every turn, Anna and Kristoff bravely push onward in a race to save their kingdom from winter's cold grip.
        """
    )
)

print(f"Prediction response:\n{res}")
