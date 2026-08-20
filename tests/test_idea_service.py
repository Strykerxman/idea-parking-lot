import pytest
from app.idea_service import create_idea, activate_idea, switch_active_idea
from app.models import IdeaStatus, IdeaDifficulty
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


def test_switch_active_idea_updates_both_ideas_and_creates_history():
    old_idea = create_idea(
        IdeaCreate(title="Current project")
    )
    new_idea = create_idea(
        IdeaCreate(title="New project")
    )

    activate_idea(old_idea.id)

    switch_active_idea(
        new_idea_id=new_idea.id,
        old_idea_new_status=IdeaStatus.PARKED,
        reason="I want to focus on the new project.",
        difficulty=IdeaDifficulty.JUST_RIGHT,
    )

    # Re-query because our original ORM objects may be stale.
    updated_old = crud.get_idea_by_id(old_idea.id)
    updated_new = crud.get_idea_by_id(new_idea.id)

    assert updated_old is not None
    assert updated_new is not None

    assert updated_old.status == IdeaStatus.PARKED
    assert updated_new.status == IdeaStatus.ACTIVE

    history = crud.get_idea_history(old_idea.id)

    assert len(history) == 1

    event = history[0]

    assert event.idea_id == old_idea.id
    assert event.from_status == IdeaStatus.ACTIVE
    assert event.to_status == IdeaStatus.PARKED
    assert event.reason == "I want to focus on the new project."
    assert event.difficulty == IdeaDifficulty.JUST_RIGHT


def test_switch_requires_active_idea():
    new_idea = create_idea(
        IdeaCreate(title="New project")
    )

    with pytest.raises(
        ValueError,
        match="There must be an active idea to swap with.",
    ):
        switch_active_idea(
            new_idea_id=new_idea.id,
            old_idea_new_status=IdeaStatus.PARKED,
            reason="Changing focus.",
            difficulty=IdeaDifficulty.JUST_RIGHT,
        )

    # Failure should not modify the target.
    updated_new = crud.get_idea_by_id(new_idea.id)

    assert updated_new is not None
    assert updated_new.status == IdeaStatus.PARKED


def test_switch_rejects_nonexistent_new_idea():
    old_idea = create_idea(
        IdeaCreate(title="Current project")
    )
    activate_idea(old_idea.id)

    with pytest.raises(ValueError, match="not found"):
        switch_active_idea(
            new_idea_id=999999,
            old_idea_new_status=IdeaStatus.PARKED,
            reason="Changing focus.",
            difficulty=IdeaDifficulty.JUST_RIGHT,
        )

    updated_old = crud.get_idea_by_id(old_idea.id)

    assert updated_old is not None
    assert updated_old.status == IdeaStatus.ACTIVE


def test_switch_requires_reason():
    old_idea = create_idea(
        IdeaCreate(title="Current project")
    )
    new_idea = create_idea(
        IdeaCreate(title="New project")
    )

    activate_idea(old_idea.id)

    with pytest.raises(
        ValueError,
        match="Reason cannot be empty.",
    ):
        switch_active_idea(
            new_idea_id=new_idea.id,
            old_idea_new_status=IdeaStatus.PARKED,
            reason="    ",
            difficulty=IdeaDifficulty.JUST_RIGHT,
        )

    updated_old = crud.get_idea_by_id(old_idea.id)
    updated_new = crud.get_idea_by_id(new_idea.id)

    assert updated_old.status == IdeaStatus.ACTIVE
    assert updated_new.status == IdeaStatus.PARKED

    assert crud.get_idea_history(old_idea.id) == []


def test_switch_rejects_active_as_old_idea_new_status():
    old_idea = create_idea(
        IdeaCreate(title="Current project")
    )
    new_idea = create_idea(
        IdeaCreate(title="New project")
    )

    activate_idea(old_idea.id)

    with pytest.raises(
        ValueError,
        match="Invalid status for the previous active idea.",
    ):
        switch_active_idea(
            new_idea_id=new_idea.id,
            old_idea_new_status=IdeaStatus.ACTIVE,
            reason="Changing focus.",
            difficulty=IdeaDifficulty.JUST_RIGHT,
        )


@pytest.mark.parametrize(
    "exit_status",
    [
        IdeaStatus.PARKED,
        IdeaStatus.COMPLETED,
        IdeaStatus.DROPPED,
    ],
)
def test_switch_allows_valid_exit_statuses(exit_status):
    old_idea = create_idea(
        IdeaCreate(title="Current project")
    )
    new_idea = create_idea(
        IdeaCreate(title="New project")
    )

    activate_idea(old_idea.id)

    switch_active_idea(
        new_idea_id=new_idea.id,
        old_idea_new_status=exit_status,
        reason="Ready to move on.",
        difficulty=IdeaDifficulty.JUST_RIGHT,
    )

    updated_old = crud.get_idea_by_id(old_idea.id)
    updated_new = crud.get_idea_by_id(new_idea.id)

    assert updated_old.status == exit_status
    assert updated_new.status == IdeaStatus.ACTIVE