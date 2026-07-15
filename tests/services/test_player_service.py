from unittest.mock import MagicMock, patch

import pytest

from app.exceptions import AlreadyExistsException, BusinessValidationException, NotFoundException
from app.schemas.player import PlayerCreate, PlayerRead, PlayerUpdate


def make_mock_player(**kwargs):
    obj = MagicMock()
    obj.id = kwargs.get("id", 1)
    obj.nickname = kwargs.get("nickname", "Caps")
    obj.real_name = kwargs.get("real_name", "Rasmus Winther")
    obj.country = kwargs.get("country", "Denmark")
    obj.age = kwargs.get("age", 25)
    obj.role = kwargs.get("role", "Mid Laner")
    obj.team_id = kwargs.get("team_id", 1)
    return obj


class TestCreatePlayer:
    @patch("app.services.player_service.repo_get_player_by_nickname")
    @patch("app.services.player_service.repo_create_player")
    def test_create_success(self, mock_create, mock_get_by_nickname, db_session):
        mock_get_by_nickname.return_value = None
        mock_create.return_value = make_mock_player()

        data = PlayerCreate(
            nickname="Caps",
            real_name="Rasmus Winther",
            country="Denmark",
            age=25,
            role="Mid Laner",
            team_id=1,
        )

        from app.services.player_service import create_player
        result = create_player(db_session, data)

        assert isinstance(result, PlayerRead)
        assert result.id == 1
        assert result.nickname == "Caps"
        mock_get_by_nickname.assert_called_once_with(db_session, "Caps")
        mock_create.assert_called_once_with(db_session, data.model_dump())

    @patch("app.services.player_service.repo_get_player_by_nickname")
    def test_create_duplicate_nickname(self, mock_get_by_nickname, db_session):
        mock_get_by_nickname.return_value = make_mock_player()

        data = PlayerCreate(
            nickname="Caps",
            real_name="Another Player",
            country="Germany",
            age=20,
            role="Support",
            team_id=2,
        )

        from app.services.player_service import create_player
        with pytest.raises(AlreadyExistsException) as exc:
            create_player(db_session, data)
        assert "Caps" in str(exc.value.message)


class TestGetPlayerById:
    @patch("app.services.player_service.repo_get_player")
    def test_get_success(self, mock_get, db_session):
        mock_get.return_value = make_mock_player()

        from app.services.player_service import get_player_by_id
        result = get_player_by_id(db_session, 1)

        assert isinstance(result, PlayerRead)
        assert result.id == 1
        mock_get.assert_called_once_with(db_session, 1)

    @patch("app.services.player_service.repo_get_player")
    def test_get_not_found(self, mock_get, db_session):
        mock_get.return_value = None

        from app.services.player_service import get_player_by_id
        with pytest.raises(NotFoundException) as exc:
            get_player_by_id(db_session, 999)
        assert "999" in str(exc.value.message)


class TestGetAllPlayers:
    @patch("app.services.player_service.repo_get_players")
    def test_pagination(self, mock_get, db_session):
        mock_get.return_value = ([make_mock_player()], 1)

        from app.services.player_service import get_all_players
        result = get_all_players(db_session)

        assert result.page == 1
        assert result.total == 1
        assert len(result.items) == 1

    @patch("app.services.player_service.repo_get_players")
    def test_sorting(self, mock_get, db_session):
        mock_get.return_value = ([make_mock_player()], 1)

        from app.services.player_service import get_all_players
        result = get_all_players(db_session, sort_by="nickname", order="desc")

        assert len(result.items) == 1
        mock_get.assert_called_once_with(
            db_session, page=1, size=10, sort_by="nickname", order="desc",
        )

    def test_invalid_sort_column(self, db_session):
        from app.services.player_service import get_all_players
        with pytest.raises(BusinessValidationException) as exc:
            get_all_players(db_session, sort_by="invalid")
        assert "sort column" in str(exc.value.message).lower()

    def test_invalid_order(self, db_session):
        from app.services.player_service import get_all_players
        with pytest.raises(BusinessValidationException) as exc:
            get_all_players(db_session, sort_by="nickname", order="bad")
        assert "sort order" in str(exc.value.message).lower()


class TestUpdatePlayer:
    @patch("app.services.player_service.repo_get_player")
    @patch("app.services.player_service.repo_get_player_by_nickname")
    @patch("app.services.player_service.repo_update_player")
    def test_update_success(self, mock_update, mock_get_by_nickname, mock_get, db_session):
        mock_get.return_value = make_mock_player()
        mock_get_by_nickname.return_value = None
        mock_update.return_value = make_mock_player(nickname="NewNick")

        from app.services.player_service import update_player
        update_data = PlayerUpdate(nickname="NewNick", age=26)
        result = update_player(db_session, 1, update_data)

        assert isinstance(result, PlayerRead)
        assert result.nickname == "NewNick"

    @patch("app.services.player_service.repo_get_player")
    def test_update_not_found(self, mock_get, db_session):
        mock_get.return_value = None

        from app.services.player_service import update_player
        with pytest.raises(NotFoundException) as exc:
            update_player(db_session, 999, PlayerUpdate())
        assert "999" in str(exc.value.message)

    @patch("app.services.player_service.repo_get_player")
    @patch("app.services.player_service.repo_get_player_by_nickname")
    def test_update_duplicate_nickname(self, mock_get_by_nickname, mock_get, db_session):
        mock_get.return_value = make_mock_player(id=1, nickname="Old")
        mock_get_by_nickname.return_value = make_mock_player(id=2, nickname="Taken")

        from app.services.player_service import update_player
        with pytest.raises(AlreadyExistsException) as exc:
            update_player(db_session, 1, PlayerUpdate(nickname="Taken"))
        assert "Taken" in str(exc.value.message)

    @patch("app.services.player_service.repo_get_player")
    @patch("app.services.player_service.repo_update_player")
    def test_update_same_nickname_skips_duplicate_check(self, mock_update, mock_get, db_session):
        existing = make_mock_player(id=1, nickname="Caps")
        mock_get.return_value = existing
        mock_update.return_value = existing

        from app.services.player_service import update_player
        update_player(db_session, 1, PlayerUpdate(nickname="Caps"))

        mock_update.assert_called_once()

    @patch("app.services.player_service.repo_get_player")
    @patch("app.services.player_service.repo_update_player")
    def test_update_no_nickname_skips_duplicate_check(self, mock_update, mock_get, db_session):
        mock_get.return_value = make_mock_player()
        mock_update.return_value = make_mock_player(age=30)

        from app.services.player_service import update_player
        update_player(db_session, 1, PlayerUpdate(age=30))

        mock_update.assert_called_once()


class TestDeletePlayer:
    @patch("app.services.player_service.repo_get_player")
    @patch("app.services.player_service.repo_delete_player")
    def test_delete_success(self, mock_delete, mock_get, db_session):
        mock_get.return_value = make_mock_player()

        from app.services.player_service import delete_player
        delete_player(db_session, 1)

        mock_get.assert_called_once_with(db_session, 1)
        mock_delete.assert_called_once()

    @patch("app.services.player_service.repo_get_player")
    def test_delete_not_found(self, mock_get, db_session):
        mock_get.return_value = None

        from app.services.player_service import delete_player
        with pytest.raises(NotFoundException) as exc:
            delete_player(db_session, 999)
        assert "999" in str(exc.value.message)
