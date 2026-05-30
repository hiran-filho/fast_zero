from dataclasses import asdict

from sqlalchemy import select

from fast_zero.models import User


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
