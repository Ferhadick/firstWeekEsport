from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from app.exceptions import BusinessValidationException, NotFoundException
from app.schemas.tournament import TournamentCreate, TournamentRead, TournamentUpdate


def make_mock_tournament(**kwargs):
    obj = MagicMock()
    obj.id = kwargs.get("id", 1)
    obj.name = kwargs.get("name", "World Championship")
    obj.game = kwargs.get("game", "League of Legends")
    obj.location = kwargs.get("location", "Berlin")
    obj.prize_pool = kwargs.get("prize_pool", Decimal("100000.00"))
    obj.start_date = kwargs.get("start_date", date(2026, 1, 1))
    obj.end_date = kwargs.get("end_date", date(2026, 6, 1))
    obj.status = kwargs.get("status", "scheduled")
    return obj


class TestCreateTournament:
    @patch("app.services.tournament_service.repo_create_tournament")
    def test_create_success(self, mock_create, db_session):
        mock_create.return_value = make_mock_tournament()
        data = TournamentCreate(
            name="World Championship",
            game="League of Legends",
            location="Berlin",
            prize_pool=Decimal("100000.00"),
            start_date=date(2026, 1, 1),
            end_date=date(2026, 6, 1),
            status="scheduled",
        )

        from app.services.tournament_service import create_tournament
        result = create_tournament(db_session, data)

        assert isinstance(result, TournamentRead)
        assert result.id == 1
        assert result.name == "World Championship"
        mock_create.assert_called_once_with(db_session, data.model_dump())


class TestGetTournamentById:
    @patch("app.services.tournament_service.repo_get_tournament")
    def test_get_success(self, mock_get, db_session):
        mock_get.return_value = make_mock_tournament()

        from app.services.tournament_service import get_tournament_by_id
        result = get_tournament_by_id(db_session, 1)

        assert isinstance(result, TournamentRead)
        assert result.id == 1
        assert result.name == "World Championship"
        mock_get.assert_called_once_with(db_session, 1)

    @patch("app.services.tournament_service.repo_get_tournament")
    def test_get_not_found(self, mock_get, db_session):
        mock_get.return_value = None

        from app.services.tournament_service import get_tournament_by_id
        with pytest.raises(NotFoundException) as exc:
            get_tournament_by_id(db_session, 999)
        assert "999" in str(exc.value.message)


class TestGetAllTournaments:
    @patch("app.services.tournament_service.repo_get_tournaments")
    def test_default_pagination(self, mock_get, db_session):
        mock_t = make_mock_tournament()
        mock_get.return_value = ([mock_t], 1)

        from app.services.tournament_service import get_all_tournaments
        result = get_all_tournaments(db_session)

        assert result.page == 1
        assert result.size == 10
        assert result.total == 1
        assert result.pages == 1
        assert len(result.items) == 1
        mock_get.assert_called_once_with(
            db_session, page=1, size=10, sort_by=None, order=None,
        )

    @patch("app.services.tournament_service.repo_get_tournaments")
    def test_custom_pagination(self, mock_get, db_session):
        mock_t = make_mock_tournament()
        mock_get.return_value = ([mock_t], 35)

        from app.services.tournament_service import get_all_tournaments
        result = get_all_tournaments(db_session, page=2, size=20)

        assert result.page == 2
        assert result.size == 20
        assert result.total == 35
        assert result.pages == 2
        mock_get.assert_called_once_with(
            db_session, page=2, size=20, sort_by=None, order=None,
        )

    @patch("app.services.tournament_service.repo_get_tournaments")
    def test_pages_rounded_up(self, mock_get, db_session):
        mock_t = make_mock_tournament()
        mock_get.return_value = ([mock_t], 11)

        from app.services.tournament_service import get_all_tournaments
        result = get_all_tournaments(db_session, page=1, size=10)

        assert result.pages == 2

    @patch("app.services.tournament_service.repo_get_tournaments")
    def test_zero_items(self, mock_get, db_session):
        mock_get.return_value = ([], 0)

        from app.services.tournament_service import get_all_tournaments
        result = get_all_tournaments(db_session)

        assert result.items == []
        assert result.total == 0
        assert result.pages == 0

    @patch("app.services.tournament_service.repo_get_tournaments")
    def test_sorting(self, mock_get, db_session):
        mock_t = make_mock_tournament()
        mock_get.return_value = ([mock_t], 1)

        from app.services.tournament_service import get_all_tournaments
        result = get_all_tournaments(db_session, sort_by="name", order="desc")

        assert len(result.items) == 1
        mock_get.assert_called_once_with(
            db_session, page=1, size=10, sort_by="name", order="desc",
        )

    def test_invalid_page(self, db_session):
        from app.services.tournament_service import get_all_tournaments
        with pytest.raises(BusinessValidationException) as exc:
            get_all_tournaments(db_session, page=0)
        assert "Page" in str(exc.value.message)

    def test_invalid_size_too_small(self, db_session):
        from app.services.tournament_service import get_all_tournaments
        with pytest.raises(BusinessValidationException) as exc:
            get_all_tournaments(db_session, size=0)
        assert "Size" in str(exc.value.message)

    def test_invalid_size_too_large(self, db_session):
        from app.services.tournament_service import get_all_tournaments
        with pytest.raises(BusinessValidationException) as exc:
            get_all_tournaments(db_session, size=101)
        assert "Size" in str(exc.value.message)

    def test_invalid_sort_column(self, db_session):
        from app.services.tournament_service import get_all_tournaments
        with pytest.raises(BusinessValidationException) as exc:
            get_all_tournaments(db_session, sort_by="invalid_column")
        assert "sort column" in str(exc.value.message).lower()

    def test_invalid_order(self, db_session):
        from app.services.tournament_service import get_all_tournaments
        with pytest.raises(BusinessValidationException) as exc:
            get_all_tournaments(db_session, sort_by="name", order="invalid")
        assert "sort order" in str(exc.value.message).lower()


class TestUpdateTournament:
    @patch("app.services.tournament_service.repo_get_tournament")
    @patch("app.services.tournament_service.repo_update_tournament")
    def test_update_success(self, mock_update, mock_get, db_session):
        mock_get.return_value = make_mock_tournament()
        mock_update.return_value = make_mock_tournament(name="Updated Name")

        from app.services.tournament_service import update_tournament
        update_data = TournamentUpdate(name="Updated Name")
        result = update_tournament(db_session, 1, update_data)

        assert isinstance(result, TournamentRead)
        assert result.name == "Updated Name"
        mock_get.assert_called_once_with(db_session, 1)
        mock_update.assert_called_once()

    @patch("app.services.tournament_service.repo_get_tournament")
    def test_update_not_found(self, mock_get, db_session):
        mock_get.return_value = None

        from app.services.tournament_service import update_tournament
        with pytest.raises(NotFoundException) as exc:
            update_tournament(db_session, 999, TournamentUpdate())
        assert "999" in str(exc.value.message)


class TestDeleteTournament:
    @patch("app.services.tournament_service.repo_get_tournament")
    @patch("app.services.tournament_service.repo_delete_tournament")
    def test_delete_success(self, mock_delete, mock_get, db_session):
        mock_get.return_value = make_mock_tournament()

        from app.services.tournament_service import delete_tournament
        delete_tournament(db_session, 1)

        mock_get.assert_called_once_with(db_session, 1)
        mock_delete.assert_called_once()

    @patch("app.services.tournament_service.repo_get_tournament")
    def test_delete_not_found(self, mock_get, db_session):
        mock_get.return_value = None

        from app.services.tournament_service import delete_tournament
        with pytest.raises(NotFoundException) as exc:
            delete_tournament(db_session, 999)
        assert "999" in str(exc.value.message)
