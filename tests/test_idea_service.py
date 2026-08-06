import pytest
from app.idea_service import create_idea
from app.models import IdeaStatus

def test_empty_title_raises_value_error():
    with pytest.raises(ValueError) as excinfo:
        create_idea("   ", "some description")

    assert "Idea title cannot be empty." in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
            create_idea("", "some description")
    
    assert "Idea title cannot be empty." in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
                create_idea("\n\t", "some description")
        
    assert "Idea title cannot be empty." in str(excinfo.value)

def test_new_idea_status_is_parked():
    idea = create_idea("title", "desc")
    assert idea.status == IdeaStatus.PARKED

def test_idea_title_description_is_stripped():
    idea = create_idea("   title ", " desc        ")
    assert idea.title == "title" and idea.description == "desc"

def test_allow_empty_description_on_creation():
    idea = create_idea("title", None)
    assert idea.description is None

def test_allow_only_title_on_creation():
    idea = create_idea("title")
    assert idea.description is None
    assert idea.title == "title"