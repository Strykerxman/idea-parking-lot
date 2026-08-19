import pytest
from unittest.mock import patch
from app.idea_service import create_idea
from app.models import IdeaStatus
from app.api.schemas import IdeaCreate
from app import crud


# mocked 'crud.add_idea' so it never tries to touch a real database connection
@patch("app.crud.add_idea")
def test_empty_title_raises_value_error(mock_add_idea):
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
