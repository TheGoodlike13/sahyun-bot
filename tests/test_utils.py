from assertpy import assert_that

from sahyun_bot.utils import identity, clean_link, choose


def test_identity():
    for o in [None, '', 13, 3.14, True]:
        assert_that(identity(o)).is_same_as(o)


def test_clean_link():
    # noinspection PyTypeChecker
    assert_that(clean_link(None)).is_empty()
    assert_that(clean_link('')).is_empty()
    assert_that(clean_link('http://localhost')).is_equal_to('https://localhost')
    assert_that(clean_link('http://www.youtube.com/watch?v=ID&playlist=')).is_equal_to('https://youtu.be/ID')


def test_choose():
    assert_that(choose('a', a='x', b='y')).is_equal_to('x')
    assert_that(choose('b', a='x', b='y')).is_equal_to('y')
    assert_that(choose('c', a='x', b='y')).is_none()
