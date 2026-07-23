from unittest.mock import MagicMock, patch

import pytest

from app.exceptions import AlreadyExistsException, BusinessValidationException, NotFoundException
from app.schemas.team import TeamCreate, TeamRead, TeamUpdate
from app.repositories.team_repository import TeamRepository


def make_mock_team(**kwargs):
    obj = MagicMock()
    obj.id = kwargs.get("id", 1)
    obj.name = kwargs.get("name", "Fnatic")
    obj.tag = kwargs.get("tag", "FNC")
    obj.country = kwargs.get("country", "UK")
    obj.founded_year = kwargs.get("founded_year", 2004)
    obj.logo_url = kwargs.get("logo_url", None)
    return obj


class TestCreateTeam:
    @patch.object(TeamRepository, "get_by_tag")
    @patch.object(TeamRepository, "create")
    def test_create_success(self, mock_create, mock_get_by_tag, db_session):
        mock_get_by_tag.return_value = None
        mock_create.return_value = make_mock_team()

        data = TeamCreate(
            name="Fnatic",
            tag="FNC",
            country="UK",
            founded_year=2004,
        )

        from app.services.team_service import create_team
        result = create_team(db_session, data)

        assert isinstance(result, TeamRead)
        assert result.id == 1
        assert result.tag == "FNC"
        mock_get_by_tag.assert_called_once_with("FNC")
        mock_create.assert_called_once_with(data.model_dump())

    @patch.object(TeamRepository, "get_by_tag")
    def test_create_duplicate_tag(self, mock_get_by_tag, db_session):
        mock_get_by_tag.return_value = make_mock_team()

        data = TeamCreate(
            name="Another Team",
            tag="FNC",
            country="Germany",
            founded_year=2010,
        )

        from app.services.team_service import create_team
        with pytest.raises(AlreadyExistsException) as exc:
            create_team(db_session, data)
        assert "FNC" in str(exc.value.message)


class TestGetTeamById:
    @patch.object(TeamRepository, "get")
    def test_get_success(self, mock_get, db_session):
        mock_get.return_value = make_mock_team()

        from app.services.team_service import get_team_by_id
        result = get_team_by_id(db_session, 1)

        assert isinstance(result, TeamRead)
        assert result.id == 1
        mock_get.assert_called_once_with(1)

    @patch.object(TeamRepository, "get")
    def test_get_not_found(self, mock_get, db_session):
        mock_get.return_value = None

        from app.services.team_service import get_team_by_id
        with pytest.raises(NotFoundException) as exc:
            get_team_by_id(db_session, 999)
        assert "999" in str(exc.value.message)


class TestGetAllTeams:
    @patch.object(TeamRepository, "get_all")
    def test_pagination(self, mock_get, db_session):
        mock_get.return_value = ([make_mock_team()], 1)

        from app.services.team_service import get_all_teams
        result = get_all_teams(db_session)

        assert result.page == 1
        assert result.size == 10
        assert result.total == 1
        assert len(result.items) == 1

    @patch.object(TeamRepository, "get_all")
    def test_sorting(self, mock_get, db_session):
        mock_get.return_value = ([make_mock_team()], 1)

        from app.services.team_service import get_all_teams
        result = get_all_teams(db_session, sort_by="name", order="asc")

        assert len(result.items) == 1
        mock_get.assert_called_once_with(
            page=1, size=10, sort_by="name", order="asc",
        )

    def test_invalid_sort_column(self, db_session):
        from app.services.team_service import get_all_teams
        with pytest.raises(BusinessValidationException) as exc:
            get_all_teams(db_session, sort_by="nonexistent")
        assert "sort column" in str(exc.value.message).lower()

    def test_invalid_order(self, db_session):
        from app.services.team_service import get_all_teams
        with pytest.raises(BusinessValidationException) as exc:
            get_all_teams(db_session, sort_by="name", order="wrong")
        assert "sort order" in str(exc.value.message).lower()


class TestUpdateTeam:
    @patch.object(TeamRepository, "get")
    @patch.object(TeamRepository, "get_by_tag")
    @patch.object(TeamRepository, "update")
    def test_update_success(self, mock_update, mock_get_by_tag, mock_get, db_session):
        mock_get.return_value = make_mock_team()
        mock_get_by_tag.return_value = None
        mock_update.return_value = make_mock_team(name="Updated Fnatic")

        from app.services.team_service import update_team
        update_data = TeamUpdate(name="Updated Fnatic", tag="UFN")
        result = update_team(db_session, 1, update_data)

        assert isinstance(result, TeamRead)
        assert result.name == "Updated Fnatic"

    @patch.object(TeamRepository, "get")
    def test_update_not_found(self, mock_get, db_session):
        mock_get.return_value = None

        from app.services.team_service import update_team
        with pytest.raises(NotFoundException) as exc:
            update_team(db_session, 999, TeamUpdate())
        assert "999" in str(exc.value.message)

    @patch.object(TeamRepository, "get")
    @patch.object(TeamRepository, "get_by_tag")
    def test_update_duplicate_tag(self, mock_get_by_tag, mock_get, db_session):
        mock_get.return_value = make_mock_team(id=1, tag="OLD")
        mock_get_by_tag.return_value = make_mock_team(id=2, tag="TAKEN")

        from app.services.team_service import update_team
        with pytest.raises(AlreadyExistsException) as exc:
            update_team(db_session, 1, TeamUpdate(tag="TAKEN"))
        assert "TAKEN" in str(exc.value.message)

    @patch.object(TeamRepository, "get")
    @patch.object(TeamRepository, "update")
    def test_update_same_tag_skips_duplicate_check(self, mock_update, mock_get, db_session):
        existing = make_mock_team(id=1, tag="FNC")
        mock_get.return_value = existing
        mock_update.return_value = existing

        from app.services.team_service import update_team
        update_team(db_session, 1, TeamUpdate(tag="FNC"))

        mock_update.assert_called_once()

    @patch.object(TeamRepository, "get")
    @patch.object(TeamRepository, "update")
    def test_update_no_tag_skips_duplicate_check(self, mock_update, mock_get, db_session):
        mock_get.return_value = make_mock_team()
        mock_update.return_value = make_mock_team(name="New Name")

        from app.services.team_service import update_team
        update_team(db_session, 1, TeamUpdate(name="New Name"))

        mock_update.assert_called_once()


class TestDeleteTeam:
    @patch.object(TeamRepository, "get")
    @patch.object(TeamRepository, "delete")
    def test_delete_success(self, mock_delete, mock_get, db_session):
        mock_get.return_value = make_mock_team()

        from app.services.team_service import delete_team
        delete_team(db_session, 1)

        mock_get.assert_called_once_with(1)
        mock_delete.assert_called_once()

    @patch.object(TeamRepository, "get")
    def test_delete_not_found(self, mock_get, db_session):
        mock_get.return_value = None

        from app.services.team_service import delete_team
        with pytest.raises(NotFoundException) as exc:
            delete_team(db_session, 999)
        assert "999" in str(exc.value.message)
