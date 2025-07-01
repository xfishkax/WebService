from concurrent import futures
import random
import grpc

from recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse,
)
import recommendations_pb2_grpc

books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="Мальтийский сокол"),
        BookRecommendation(id=2, title="Убийство в Восточном экспрессе"),
        BookRecommendation(id=3, title="Собака Баскервилей"),
    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(id=4, title="Дюна"),
        BookRecommendation(id=5, title="Думай и богатей"),

    ],
    BookCategory.SELF_HELP: [
        BookRecommendation(id=6, title="Сила настоящего"),
        BookRecommendation(id=7, title="Атомные привычки"),
        BookRecommendation(id=8, title="Психология влияния"),
        BookRecommendation(id=9, title="Эссенциализм"),
        BookRecommendation(id=10, title="Магия утра"),
        BookRecommendation(id=11, title="Начни с почему"),
        BookRecommendation(id=12, title="Семь навыков высокоэффективных людей"),
        BookRecommendation(id=13, title="Как завоёвывать друзей и оказывать влияние"),
        BookRecommendation(id=14, title="Человек в поисках смысла"),

    ],
}

class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")
        books = books_by_category[request.category]
        num = min(request.max_results, len(books))
        return RecommendationResponse(recommendations=random.sample(books, num))

def serve():
    print("✅ Recommendations service is running on port 50051...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
