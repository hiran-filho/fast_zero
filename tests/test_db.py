from dataclasses import asdict

from sqlalchemy import select

from fast_zero.database import get_session
from fast_zero.models import User


def test_db_session():
    gen_session = get_session()
    session = next(gen_session)

    # Ping with DB
    result = session.execute(select(1)).scalar()
    assert result == 1

    # continue to use the session for other operations if needed
    try:
        # This should raise StopIteration since the
        # generator should be exhausted
        next(gen_session)
    except StopIteration:
        pass


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        user_new = User(
            username='alice', email='alice@example.com', password='password123'
        )
        session.add(user_new)
        session.commit()
    # session.refresh(user)
    user = session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'password123',
        'created_at': time,
    }
