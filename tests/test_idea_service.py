import pytest
from unittest.mock import patch
from app.idea_service import create_idea, activate_idea
from app.models import IdeaStatus
from app.api.schemas import IdeaCreate
from app import crud


def test_empty_title_raises_value_error():
    # If using mode="after" validator, Pydantic raises ValidationError instead of ValueError
    from pydantic import ValidationError
    
    with pytest.raises((ValueError, ValidationError)) as excinfo:
        create_idea(IdeaCreate(title="   ", description="some description"))
    assert "Idea title cannot be empty." in str(excinfo.value)

    with pytest.raises((ValueError, ValidationError)) as excinfo:
        create_idea(IdeaCreate(title="", description="some description"))
    assert "Idea title cannot be empty." in str(excinfo.value)

    with pytest.raises((ValueError, ValidationError)) as excinfo:
        create_idea(IdeaCreate(title="\n\t", description="some description"))
    assert "Idea title cannot be empty." in str(excinfo.value)


def test_new_idea_added_to_db():
    idea = create_idea(IdeaCreate(title="title", description="desc"))
    assert idea.id is not None
    all_ideas = crud.get_all_ideas()
    assert len(all_ideas) == 1
    assert all_ideas[0].title == "title"


def test_new_idea_status_is_parked():
    idea = create_idea(IdeaCreate(title="title", description="desc"))
    assert idea.status == IdeaStatus.PARKED


def test_idea_title_description_is_stripped():
    idea = create_idea(IdeaCreate(title="   title ", description=" desc        "))
    assert idea.title == "title"
    assert idea.description == "desc"


def test_allow_empty_description_on_creation():
    idea = create_idea(IdeaCreate(title="title", description=None))
    assert idea.description is None


def test_allow_only_title_on_creation():
    idea = create_idea(IdeaCreate(title="title"))
    assert idea.description is None
    assert idea.title == "title"


def test_idea_can_be_activated():
    idea = create_idea(IdeaCreate(title="title"))
    assert idea.id is not None
    assert idea.status == IdeaStatus.PARKED

    activate_idea(idea.id)
    # assert idea.status == IdeaStatus.ACTIVE # status not updated because idea object is stale, yet updated in db

    updated_idea = crud.get_idea_by_id(idea.id)

    assert updated_idea.status == IdeaStatus.ACTIVE


def test_activating_an_idea_when_another_is_active_raises_value_error():
    idea1 = create_idea(IdeaCreate(title="title1"))
    idea2 = create_idea(IdeaCreate(title="title2"))

    activate_idea(idea1.id)

    with pytest.raises(ValueError) as excinfo:
        activate_idea(idea2.id)
    assert "Another idea is already active." in str(excinfo.value)


def test_nonexistent_idea_activation_raises_value_error():
    with pytest.raises(ValueError) as excinfo:
        activate_idea(9999)
    assert "Idea with id 9999 not found." in str(excinfo.value)