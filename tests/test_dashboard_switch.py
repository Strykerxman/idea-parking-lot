from fastapi.testclient import TestClient

from app import crud
from app.api.schemas import IdeaCreate
from app.idea_service import activate_idea, create_idea
from app.main import app
from app.models import IdeaDifficulty, IdeaStatus


client = TestClient(app)


def test_dashboard_shows_make_active_when_there_is_no_active_idea():
    create_idea(IdeaCreate(title="Parked project"))

    response = client.get("/")

    assert response.status_code == 200
    assert "Make Active" in response.text
    assert "Switch to this idea" not in response.text


def test_switch_form_shows_allowed_status_and_difficulty_choices():
    active_idea = create_idea(IdeaCreate(title="Current project"))
    create_idea(IdeaCreate(title="Next project"))
    activate_idea(active_idea.id)

    response = client.get("/")

    assert response.status_code == 200
    assert "Switch to this idea" in response.text
    assert "Make Active" not in response.text
    assert f'value="{IdeaStatus.PARKED.value}"' in response.text
    assert f'value="{IdeaStatus.COMPLETED.value}"' in response.text
    assert f'value="{IdeaStatus.DROPPED.value}"' in response.text
    assert f'value="{IdeaDifficulty.TOO_EASY.value}"' in response.text
    assert f'value="{IdeaDifficulty.JUST_RIGHT.value}"' in response.text
    assert f'value="{IdeaDifficulty.TOO_HARD.value}"' in response.text


def test_switch_route_switches_ideas_and_redirects_to_dashboard():
    active_idea = create_idea(IdeaCreate(title="Current project"))
    next_idea = create_idea(IdeaCreate(title="Next project"))
    activate_idea(active_idea.id)

    response = client.post(
        f"/switch/{next_idea.id}",
        data={
            "old_idea_new_status": IdeaStatus.COMPLETED.value,
            "reason": "The current project is finished.",
            "difficulty": IdeaDifficulty.JUST_RIGHT.value,
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/"
    assert crud.get_idea_by_id(active_idea.id).status == IdeaStatus.COMPLETED
    assert crud.get_idea_by_id(next_idea.id).status == IdeaStatus.ACTIVE


def test_switch_route_renders_service_errors_on_dashboard():
    next_idea = create_idea(IdeaCreate(title="Next project"))

    response = client.post(
        f"/switch/{next_idea.id}",
        data={
            "old_idea_new_status": IdeaStatus.PARKED.value,
            "reason": "Changing focus.",
            "difficulty": IdeaDifficulty.JUST_RIGHT.value,
        },
    )

    assert response.status_code == 409
    assert 'role="alert"' in response.text
    assert "There must be an active idea to swap with." in response.text
