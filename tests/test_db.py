from sqlalchemy import select

from fast_zero.models import Todo, User


def test_create_user(session):
    user = User(
        username='teste',
        password='secret',
        email='test@example',
    )

    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.username == 'teste'))

    assert result.id == 1


def test_create_todo(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test description',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
