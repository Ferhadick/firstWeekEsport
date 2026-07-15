from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

import pytest

from app.exceptions import BusinessValidationException, NotFoundException
from app.schemas.match import MatchCreate, MatchRead, MatchUpdate


def make_mock_match(**kwargs):
    obj = MagicMock()
    obj.id = kwargs.get("id", 1)
    obj.tournament_id = kwargs.get("tournament_id", 1)
    obj.team1_id = kwargs.get("team1_id", 1)
    obj.team2_id = kwargs.get("team2_id", 2)
    obj.winner_id = kwargs.get("winner_id", None)
    obj.scheduled_at = kwargs.get(
        "scheduled_at",
        datetime.now(timezone.utc) + timedelta(days=7),
    )
    obj.status = kwargs.get("status", "scheduled")
    obj.score_team1 = kwargs.get("score_team1", None)
    obj.score_team2 = kwargs.get("score_team2", None)
    return obj


class TestCreateMatch:
    @patch("app.services.match_service.repo_create_match")
    def test_create_success(self, mock_create, db_session):
        future = datetime.now(timezone.utc) + timedelta(days=7)
        mock_create.return_value = make_mock_match(scheduled_at=future)

        data = MatchCreate(
            tournament_id=1,
            team1_id=1,
            team2_id=2,
            scheduled_at=future,
            status="scheduled",
        )

        from app.services.match_service import create_match
        result = create_match(db_session, data)

        assert isinstance(result, MatchRead)
        assert result.id == 1
        mock_create.assert_called_once_with(db_session, data.model_dump())


class TestGetMatchById:
    @patch("app.services.match_service.repo_get_match")
    def test_get_success(self, mock_get, db_session):
        mock_get.return_value = make_mock_match()

        from app.services.match_service import get_match_by_id
        result = get_match_by_id(db_session, 1)

        assert isinstance(result, MatchRead)
        assert result.id == 1
        mock_get.assert_called_once_with(db_session, 1)

    @patch("app.services.match_service.repo_get_match")
    def test_get_not_found(self, mock_get, db_session):
        mock_get.return_value = None

        from app.services.match_service import get_match_by_id
        with pytest.raises(NotFoundException) as exc:
            get_match_by_id(db_session, 999)
        assert "999" in str(exc.value.message)


class TestGetAllMatches:
    @patch("app.services.match_service.repo_get_matches")
    def test_pagination(self, mock_get, db_session):
        mock_get.return_value = ([make_mock_match()], 1)

        from app.services.match_service import get_all_matches
        result = get_all_matches(db_session)

        assert result.page == 1
        assert result.total == 1
        assert len(result.items) == 1

    @patch("app.services.match_service.repo_get_matches")
    def test_sorting(self, mock_get, db_session):
        mock_get.return_value = ([make_mock_match()], 1)

        from app.services.match_service import get_all_matches
        result = get_all_matches(db_session, sort_by="scheduled_at", order="asc")

        assert len(result.items) == 1
        mock_get.assert_called_once_with(
            db_session, page=1, size=10, sort_by="scheduled_at", order="asc",
        )

    def test_invalid_sort_column(self, db_session):
        from app.services.match_service import get_all_matches
        with pytest.raises(BusinessValidationException) as exc:
            get_all_matches(db_session, sort_by="invalid")
        assert "sort column" in str(exc.value.message).lower()

    def test_invalid_order(self, db_session):
        from app.services.match_service import get_all_matches
        with pytest.raises(BusinessValidationException) as exc:
            get_all_matches(db_session, sort_by="id", order="wrong")
        assert "sort order" in str(exc.value.message).lower()


class TestUpdateMatch:
    @patch("app.services.match_service.repo_get_match")
    @patch("app.services.match_service.repo_update_match")
    def test_update_success(self, mock_update, mock_get, db_session):
        mock_get.return_value = make_mock_match()
        mock_update.return_value = make_mock_match(status="completed")

        from app.services.match_service import update_match
        update_data = MatchUpdate(status="completed")
        result = update_match(db_session, 1, update_data)

        assert isinstance(result, MatchRead)
        assert result.status == "completed"
        mock_get.assert_called_once_with(db_session, 1)
        mock_update.assert_called_once()

    @patch("app.services.match_service.repo_get_match")
    def test_update_not_found(self, mock_get, db_session):
        mock_get.return_value = None

        from app.services.match_service import update_match
        with pytest.raises(NotFoundException) as exc:
            update_match(db_session, 999, MatchUpdate())
        assert "999" in str(exc.value.message)


class TestDeleteMatch:
    @patch("app.services.match_service.repo_get_match")
    @patch("app.services.match_service.repo_delete_match")
    def test_delete_success(self, mock_delete, mock_get, db_session):
        mock_get.return_value = make_mock_match()

        from app.services.match_service import delete_match
        delete_match(db_session, 1)

        mock_get.assert_called_once_with(db_session, 1)
        mock_delete.assert_called_once()

    @patch("app.services.match_service.repo_get_match")
    def test_delete_not_found(self, mock_get, db_session):
        mock_get.return_value = None

        from app.services.match_service import delete_match
        with pytest.raises(NotFoundException) as exc:
            delete_match(db_session, 999)
        assert "999" in str(exc.value.message)
