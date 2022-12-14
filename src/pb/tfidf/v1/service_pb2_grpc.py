# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from tfidf.v1 import service_pb2 as tfidf_dot_v1_dot_service__pb2


class MovieGenreStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Predict = channel.unary_unary(
                '/tfidf.MovieGenre/Predict',
                request_serializer=tfidf_dot_v1_dot_service__pb2.PredictRequest.SerializeToString,
                response_deserializer=tfidf_dot_v1_dot_service__pb2.PredictReply.FromString,
                )
        self.Train = channel.unary_unary(
                '/tfidf.MovieGenre/Train',
                request_serializer=tfidf_dot_v1_dot_service__pb2.TrainRequest.SerializeToString,
                response_deserializer=tfidf_dot_v1_dot_service__pb2.TrainReply.FromString,
                )


class MovieGenreServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Predict(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Train(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MovieGenreServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Predict': grpc.unary_unary_rpc_method_handler(
                    servicer.Predict,
                    request_deserializer=tfidf_dot_v1_dot_service__pb2.PredictRequest.FromString,
                    response_serializer=tfidf_dot_v1_dot_service__pb2.PredictReply.SerializeToString,
            ),
            'Train': grpc.unary_unary_rpc_method_handler(
                    servicer.Train,
                    request_deserializer=tfidf_dot_v1_dot_service__pb2.TrainRequest.FromString,
                    response_serializer=tfidf_dot_v1_dot_service__pb2.TrainReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tfidf.MovieGenre', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MovieGenre(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Predict(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tfidf.MovieGenre/Predict',
            tfidf_dot_v1_dot_service__pb2.PredictRequest.SerializeToString,
            tfidf_dot_v1_dot_service__pb2.PredictReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Train(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tfidf.MovieGenre/Train',
            tfidf_dot_v1_dot_service__pb2.TrainRequest.SerializeToString,
            tfidf_dot_v1_dot_service__pb2.TrainReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
