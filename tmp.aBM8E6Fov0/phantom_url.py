import operator as op

from urllib.parse import (
    ParseResult,
    urlparse,
)

import attrs
import pytest

from phantom import Phantom
from phantom.fn import compose2


def is_url_address(value: str) -> bool:
    return any(urlparse(value))


class URL(str, Phantom, predicate=is_url_address):
    pass


# presume that an empty URL is a nonsense
def test_empty_url():
    with pytest.raises(TypeError, match="Could not parse .* from ''"):
        ReachableURL.parse("")


# is it enough now?
def test_url():
    assert URL.parse("http://")


scheme_and_netloc = op.attrgetter("scheme", "netloc")


def has_scheme_and_netloc(value: ParseResult) -> bool:
    return all(scheme_and_netloc(value))


# need a bit of FP magic 🧙 here
class ReachableURL(URL, predicate=compose2(has_scheme_and_netloc, urlparse)):
    pass


def test_empty_reachable_url():
    with pytest.raises(TypeError, match="Could not parse .* from ''"):
        ReachableURL.parse("")


def test_reachable_url_probably_wrong_host():
    assert ReachableURL.parse("http://example")


def test_reachable_url():
    assert ReachableURL.parse("http://example.com")


def test_reachable_url_without_scheme():
    with pytest.raises(TypeError, match="Could not parse .* from 'example.com'"):
        ReachableURL.parse("example.com")


# constructor works too
def test_constructor():
    assert ReachableURL("http://example.com")


# bit it *is* `str`
def test_url_is_str():
    assert isinstance(ReachableURL("http://example.com"), str)


# now we can write *Entity* as a plain old class

# I'm lazy...


@attrs.define
class Person:
    homepage: ReachableURL


def test_person():
    person = Person(homepage=ReachableURL("https://example.com/index.html"))

    assert person.homepage


def greet(person: Person) -> None:
    print(f"Hello! I will definitely visit you at {person.homepage}.")


if __name__ == "__main__":
    greet(Person(homepage=ReachableURL.parse("tg://resolve?username")))
