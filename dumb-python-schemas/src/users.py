from typing import TypedDict, TypeVar

import attrs
import pendulum
from phantom.datetime import TZAware

EmailAddress = str


@attrs.define(frozen=True)
class Can:
    description: str


@attrs.define
class User:
    id: int
    member_since: TZAware
    full_name: str
    email: EmailAddress
    permissions: tuple[Can, ...]


E = TypeVar("E", bound=User)


class Schema(TypedDict):
    """A *Schema* does one thing - it "looks up itself" in passed Entity
    """


def conform(entity: E, S: Schema) -> Schema:
    # names = S.__required_keys__
    # values = op.attrgetter(*names)

    data = attrs.asdict(entity)

    return S(**{k: data[k] for k in S.__required_keys__})
    # return S(**{n: getattr(entity, n) for n in S.__required_keys__})

    # return S(**dict(zip(names, values(entity))))
    # return S(**{n: v for n, v in data.items() if n in S.__required_keys__})


class UserSchema(TypedDict, Schema):
    id: int
    member_since: TZAware
    full_name: str
    email: EmailAddress


me = User(
    id=42,
    member_since=pendulum.now(),
    full_name="Anthony",
    email="anthony@example.com",
    permissions=(
        Can("read_users"),
        Can("manage_users"),
    ),
)


def test_conform_user_schema():
    assert conform(me, UserSchema) == {
        "id": 42,
        "member_since": me.member_since,
        "full_name": "Anthony",
        "email": "anthony@example.com",
    }


class AnonymousUserSchema(TypedDict):
    full_name: str


class AdminUserSchema(TypedDict):
    id: int
    member_since: TZAware
    full_name: str
    email: EmailAddress
    permissions: tuple[Can, ...]


def test_conform_anonymous_user_schema():
    assert conform(me, AnonymousUserSchema) == {"full_name": "Anthony"}


def test_conform_admin_user_schema():
    assert conform(me, AdminUserSchema) == {
        "email": "anthony@example.com",
        "full_name": "Anthony",
        "id": 42,
        "member_since": me.member_since,
        "permissions": (
            {"description": "read_users"},
            {"description": "manage_users"},
        ),
    }
