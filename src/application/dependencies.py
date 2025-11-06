from src.adapter.outgoing.relational_db_url_repository import RelationalDbUrlRepository
from src.application.port.incoming.ShorteningService import ShorteningService
from src.application.service.url_shortening_service import UrlShorteningService


# Application services
shortening_service: ShorteningService = UrlShorteningService(
    url_repository=RelationalDbUrlRepository()
)
