from gobblegobble.bot import gobble_listen
from gobblekarma.models import KarmaFor, Karma


@gobble_listen("(.*)\+\+ for (.*)")
def upvote_for(message, recipient, karma_for):
    karma = KarmaFor.increment(recipient, karma_for)
    message.respond(karma)


@gobble_listen("(.*)\+\+")
def upvote(message, recipient):
    if message.text.find("++ for ") < 0:
        karma = Karma.increment(recipient)
        message.respond(karma)


# slack smart edits "--"
@gobble_listen("(.*)— for (.*)")
@gobble_listen("(.*)\-\- for (.*)")
def downvote_for(message, recipient, karma_for):
    karma = KarmaFor.decrement(recipient, karma_for)
    message.respond(karma)


# slack smart edits "--"
@gobble_listen("(.*)—")
@gobble_listen("(.*)\-\-")
def downvote(message, recipient):
    if message.text.find("-- for ") < 0 and message.text.find("— for ") < 0:
        karma = Karma.decrement(recipient)
        message.respond(karma)


@gobble_listen("karma")
def get_top_ten(message):
    if len(message) > 5:
        return
    resp  = ""
    tops = []
    i = 1
    for karma in Karma.objects.all().order_by('-amount'):
        tops.append("%s. %s\n" % (i, str(karma)))
        i = i+1
    resp = "%s%s" % (resp, "".join(tops))
    message.respond(resp)
    return resp


@gobble_listen("karma (.*)")
def get_karma_for(message, recipient):
    karma = Karma.find_or_create_by_recipient(recipient)
    resp = str(karma)
    fors = []
    for kf in KarmaFor.objects.filter(karma=karma).order_by('-amount'):
        fors.append("\n%s" % kf._substr())
    resp = "%s%s" % (resp, "".join(fors))
    message.respond(resp)
    return resp
