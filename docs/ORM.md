Stale ORM Objects
-----------------

An ORM object represents database state at the time it was loaded or
modified within its SQLAlchemy session. It is not a live pointer to the
database.

For example, `test_idea_can_be_activated` creates an Idea and receives
an ORM object whose status is `PARKED`.

`activate_idea(idea.id)` then opens another session, loads the same
database row into another ORM object, changes its status to `ACTIVE`,
and commits.

The original `idea` object in the test is not automatically updated,
so `idea.status` can still be `PARKED`.

To verify the persisted change, the test queries the database again and
checks the newly loaded object's status.