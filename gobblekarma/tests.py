from django.test import TestCase

from gobblegobble.bot import Message
from gobblekarma.bot_responder import upvote, upvote_for, downvote, downvote_for, \
    get_karma_for
from gobblekarma.models import Karma, KarmaFor


class TestKarma(TestCase):

    def test_recipient_is_always_lowercase(self):

        karma = Karma()
        karma.recipient = 'FoOBar'
        karma.amount = karma.amount+1
        karma.save()
        self.assertEqual(karma.recipient, 'foobar')

    def test_find_or_create_by_recipient(self):
        karma1 = Karma.find_or_create_by_recipient('testfinder1')
        karma2 = Karma.objects.get(recipient='testfinder1')
        self.assertEqual(karma2, karma1)
        self.assertEqual(Karma.objects.filter(recipient='testfinder1').count(), 1)

    def test_increment(self):

        karma = Karma.increment('testincr1')
        self.assertEqual(karma.amount,1)
        karma = Karma.increment('teSTinCr1')
        self.assertEqual(karma.amount,2)

    def test_decrement(self):

        karma = Karma.decrement('testdecr1')
        self.assertEqual(karma.amount,-1)
        karma = Karma.decrement('teSTdecR1')
        self.assertEqual(karma.amount,-2)

    def test_to_str(self):

        karma = Karma.increment('teststr1')
        self.assertEqual(karma.__str__(),"teststr1 has 1 point")
        karma = Karma.increment('teststr1')
        self.assertEqual(karma.__str__(),"teststr1 has 2 points")


class TestKarmaFor(TestCase):

    def test_for_is_always_lowercase(self):

        karma = Karma.increment('testfor1')
        karma_for = KarmaFor()
        karma_for.karma = karma
        karma_for.karma_for = "STUFF"
        karma_for.amount = karma_for.amount+1
        karma_for.save()
        self.assertEqual(karma_for.karma_for, "stuff")

    def test_find_or_create_by_recipient_and_for(self):
        karma_for1 = KarmaFor.find_or_create_by_recipient_and_for('testkarmaforfind1','stuff')
        karma = Karma.objects.get(recipient='testkarmaforfind1')
        karma_for2 = KarmaFor.objects.get(karma=karma, karma_for='stuff')
        self.assertEqual(karma_for2, karma_for1)
        self.assertEqual(KarmaFor.objects.filter(karma=karma, karma_for='stuff').count(),1)

    def test_increment(self):

        karma = Karma.increment('testforincr1')
        karma_for = KarmaFor.increment('testforincr1', 'some stuff')
        karma.refresh_from_db()
        self.assertEqual(karma.amount, 2)
        self.assertEqual(karma_for.amount, 1)
        self.assertEqual(karma_for.karma, karma)
        karma_for = KarmaFor.increment('testFORincr1', 'some stuff')
        self.assertEqual(karma_for.karma.amount, 3)
        self.assertEqual(karma_for.amount, 2)
        self.assertEqual(karma_for.karma, karma)

    def test_increment_autocreates_karma(self):

        self.assertRaises(Karma.DoesNotExist, Karma.objects.get, recipient='testforincr2')
        karma_for = KarmaFor.increment('testforincr2', 'testforincr2 things')
        self.assertEqual(karma_for.amount, 1)
        self.assertEqual(karma_for.karma.amount, 1)

    def test_decrement(self):

        karma = Karma.decrement('testfordecr1')
        karma_for = KarmaFor.decrement('testfordecr1', 'some stuff')
        karma.refresh_from_db()
        self.assertEqual(karma.amount, -2)
        self.assertEqual(karma_for.amount, -1)
        self.assertEqual(karma_for.karma, karma)
        karma_for = KarmaFor.decrement('testForDecr1', 'some stuff')
        self.assertEqual(karma_for.karma.amount, -3)
        self.assertEqual(karma_for.amount, -2)
        self.assertEqual(karma_for.karma, karma)

    def test_decrement_autocreates_karma(self):

        self.assertRaises(Karma.DoesNotExist, Karma.objects.get, recipient='testfordecr2')
        karma_for = KarmaFor.decrement('testforincr2', 'testforincr2 things')
        self.assertEqual(karma_for.amount, -1)
        self.assertEqual(karma_for.karma.amount, -1)

    def test_unique_together_increments_and_not_new(self):

        karma_for = KarmaFor.increment('testforincr3', 'testforincr3 things')
        self.assertEqual(KarmaFor.objects.filter(karma=karma_for.karma, karma_for='testforincr3 things').count(),1)
        self.assertEqual(karma_for.amount, 1)
        self.assertEqual(karma_for.karma.amount, 1)
        karma_for = KarmaFor.increment('testforincr3', 'testforincr3 things')
        self.assertEqual(KarmaFor.objects.filter(karma=karma_for.karma, karma_for='testforincr3 things').count(),1)
        self.assertEqual(karma_for.amount, 2)
        self.assertEqual(karma_for.karma.amount, 2)

    def test_to_str(self):

        karma_for = KarmaFor.increment('testforstr1', 'testforstr1 things')
        self.assertEqual(karma_for.__str__(), 'testforstr1 has 1 point, 1 of which is for testforstr1 things')
        karma_for = KarmaFor.increment('testforstr1', 'testforstr1 things')
        self.assertEqual(karma_for.__str__(), 'testforstr1 has 2 points, 2 of which are for testforstr1 things')


class TestResponders(TestCase):

    def test_upvote_for(self):

        upvote_for(Message(), 'testgivekarmafor1', 'some stuff')
        karma = Karma.objects.get(recipient='testgivekarmafor1')
        karma_for = KarmaFor.objects.get(karma=karma, karma_for='some stuff')
        self.assertEqual(karma_for.amount,1)
        self.assertEqual(karma.amount,1)

    def test_upvote(self):

        message = Message()
        message.text = "testgivekarma1++"
        upvote(message, "testgivekarma1")
        karma = Karma.objects.get(recipient='testgivekarma1')
        self.assertEqual(karma.amount,1)

    def test_downvote_for(self):

        downvote_for(Message(), 'testdownvotefor1', 'some stuff')
        karma = Karma.objects.get(recipient='testdownvotefor1')
        karma_for = KarmaFor.objects.get(karma=karma, karma_for='some stuff')
        self.assertEqual(karma_for.amount,-1)
        self.assertEqual(karma.amount,-1)

    def test_downvote(self):

        message = Message()
        message.text = "testdownvotekarma1--"
        downvote(message, "testdownvotekarma1")
        karma = Karma.objects.get(recipient='testdownvotekarma1')
        self.assertEqual(karma.amount,-1)

    def test_get_top_ten(self):
        pass

    def test_get_karma_for(self):
        KarmaFor.increment("testkarmaforintrospec1", "stuff1")
        KarmaFor.increment("testkarmaforintrospec1", "stuff1")
        KarmaFor.increment("testkarmaforintrospec1", "stuff1")
        KarmaFor.increment("testkarmaforintrospec1", "stuff2")
        KarmaFor.decrement("testkarmaforintrospec1", "stuff1")
        KarmaFor.decrement("testkarmaforintrospec1", "badstuff1")
        resp = get_karma_for(Message(), "testkarmaforintrospec1")
        self.assertEquals(resp, "testkarmaforintrospec1 has 2 points\n2 of which are for stuff1\n1 of which is for stuff2\n-1 of which is for badstuff1")
