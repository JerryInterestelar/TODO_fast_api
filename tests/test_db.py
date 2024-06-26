from sqlalchemy import select

from fast_zero.models import User


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
