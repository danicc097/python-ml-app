import json

from src.pb.tfidf.v1 import service_pb2
from src.pb.tfidf.v1 import service_pb2_grpc
import grpc

channel = grpc.insecure_channel("localhost:50051")
stub = service_pb2_grpc.MovieGenreStub(channel)
res: service_pb2.PredictReply = stub.Predict(
    service_pb2.PredictRequest(
        synopsis="""
Asian horror cinema often depicts stomach-churning scenes of gore and zombie outbreaks quite vividly and The Sadness ticks all the right boxes.

Chaos and anarchy descend on the city of Taipei as residents turn into mass killers. In the wake of such a deadly viral pandemic, Jim and Kat are a young couple who seek to find each other. Violence, killing and massacre only seem to rise while the government and authorities remain complacent.

Among the most gruesome horror movies of 2022, The Sadness lives up to its name and is not for the faint-hearted. In fact, a trigger warning is also issued at the beginning for those who may not be able to endure watching all the slashing and blood.
"""
    )
)

print("Predictions:")
[print(f"{i+1}: {prediction.genre}") for i, prediction in enumerate(res.predictions)]
# 1: psychedelic
# 2: depressing
# 3: murder
# 4: comedy
# 5: revenge
# 6: violence
# 7: flashback
# 8: cult
