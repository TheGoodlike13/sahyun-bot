from assertpy import assert_that
from httmock import HTTMock

from sahyun_bot.commands.admin import Index, Rank
from sahyun_bot.users_settings import UserRank
from tests.mock_customsforge import customsforge


def test_require_admin(commander, hook):
    for command in ['!lock', '!index', '!rank']:
        with commander.executest(hook, command, 'goodlikebot'):
            hook.assert_silent_failure()


def test_lock_unlock(commander, hook):
    with commander.executest(hook, '!lock'):
        hook.assert_success('Bot is now in ADMIN only mode')

    # even basic commands are unauthorized
    with commander.executest(hook, '!time', 'goodlikebot'):
        hook.assert_silent_failure()

    with commander.executest(hook, '!lock'):
        hook.assert_success('Bot no longer in ADMIN only mode')

    # functionality restored
    with commander.executest(hook, '!time', 'goodlikebot'):
        hook.assert_success()


def test_index(tl, hook):
    with HTTMock(customsforge), Index(tl=tl).executest(hook):
        hook.assert_success('CDLCs indexed')

    tl.set_use_elastic(False)

    with HTTMock(customsforge), Index(tl=tl).executest(hook):
        hook.assert_failure('CDLCs could not be indexed')


def test_rank(users, hook):
    with Rank(us=users).executest(hook, args=''):
        hook.assert_failure('Try !rank RANK NICK')

    with Rank(us=users).executest(hook, args='just_rank'):
        hook.assert_failure('Try !rank RANK NICK')

    with Rank(us=users).executest(hook, args='BAD_RANK goodlikebot'):
        hook.assert_failure('BAD_RANK is not a valid rank')

    with Rank(us=users).executest(hook, args='BAN goodlikebot'), users._manual('goodlikebot'):
        hook.assert_success('goodlikebot is now BAN')
        assert_that(users.rank('goodlikebot')).is_equal_to(UserRank.BAN)

    users.set_use_elastic(False)

    with Rank(us=users).executest(hook, args='ADMIN goodlikebot'):
        hook.assert_failure('Rank could not be set')


def test_rank_shorthand(commander, hook):
    with commander.executest(hook, '!ban goodlikebot'), commander._users._manual('goodlikebot'):
        hook.assert_success('goodlikebot is now BAN')
        assert_that(commander._users.rank('goodlikebot')).is_equal_to(UserRank.BAN)
