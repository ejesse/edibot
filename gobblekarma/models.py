from django.db import models


class Karma(models.Model):

    recipient = models.CharField(unique=True, blank=False, max_length=255)
    amount = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.recipient = self.recipient.lower()
        super(Karma, self).save(*args, **kwargs) # Call the "real" save()

    @staticmethod
    def find_or_create_by_recipient(recipient):
        recipient = recipient.lower()
        try:
            karma = Karma.objects.get(recipient=recipient)
        except Karma.DoesNotExist:
            karma = Karma(recipient=recipient)
            karma.save()
        return karma

    @staticmethod
    def increment(recipient):
        recipient = recipient.lower()
        karma = Karma.find_or_create_by_recipient(recipient)
        karma.amount = karma.amount+1
        karma.save()
        return karma

    @staticmethod
    def decrement(recipient):
        recipient = recipient.lower()
        karma = Karma.find_or_create_by_recipient(recipient)
        karma.amount = karma.amount-1
        karma.save()
        return karma

    def __str__(self):
        points = "points"
        if self.amount == 1 or self.amount == -1:
            points = "point"
        return "%s has %s %s" % (self.recipient, self.amount, points)


class KarmaFor(models.Model):

    karma = models.ForeignKey(Karma)
    karma_for = models.CharField(blank=False, max_length=255)
    amount = models.IntegerField(default=0)

    unique_together = (("karma", "karma_for"),)

    def save(self, *args, **kwargs):
        self.karma_for = self.karma_for.lower()
        super(KarmaFor, self).save(*args, **kwargs) # Call the "real" save()

    def _substr(self):
        is_are = 'are'
        if self.amount == 1 or self.amount == -1:
            is_are = 'is'
        return "%s of which %s for %s" % (self.amount, is_are, self.karma_for)

    def __str__(self):
        return "%s, %s" % (self.karma.__str__(), self._substr())

    @staticmethod
    def find_or_create_by_recipient_and_for(recipient, karma_for):
        recipient = recipient.lower()
        karma = Karma.find_or_create_by_recipient(recipient)
        try:
            karma_for = KarmaFor.objects.get(karma=karma, karma_for=karma_for)
        except KarmaFor.DoesNotExist:
            karma_for = KarmaFor(karma=karma, karma_for=karma_for)
            karma_for.save()
        return karma_for

    @staticmethod
    def increment(recipient, karma_for):
        recipient = recipient.lower()
        Karma.increment(recipient)
        karma_for = KarmaFor.find_or_create_by_recipient_and_for(recipient, karma_for)
        karma_for.amount = karma_for.amount+1
        karma_for.save()
        return karma_for

    @staticmethod
    def decrement(recipient, karma_for):
        recipient = recipient.lower()
        Karma.decrement(recipient)
        karma_for = KarmaFor.find_or_create_by_recipient_and_for(recipient, karma_for)
        karma_for.amount = karma_for.amount-1
        karma_for.save()
        return karma_for

