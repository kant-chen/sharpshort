import datetime
import base62
import string

from django.db import models

LETTERS = string.ascii_letters + "0123456789"


class Shorting(models.Model):
    MAX_LETTER = 5

    path = models.CharField(max_length=5, unique=True, help_text="The shortening path")
    destination = models.URLField(
        null=True, help_text="The destination URL to be redirected"
    )
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{'V' if self.is_valid else 'X'} {self.path} ==> {self.destination}"

    @classmethod
    def shorten(cls, dest_url):
        now = datetime.datetime.now().timestamp()
        rounded_time = round(now)
        return base62.encode(rounded_time, 5)[1:6]

    @classmethod
    def pre_generate(cls, count=100):
        last_shorting = cls.objects.order_by("-created_at").first()
        if not last_shorting:
            last_shorting = cls.objects.create(
                path=LETTERS[0] * cls.MAX_LETTER, is_valid=False
            )
        next_path = last_shorting.path
        cnt = 0
        for i in range(count):
            next_path = cls.get_next_path(next_path)
            cls.objects.create(path=next_path, is_valid=False)
            cnt += 1

    @classmethod
    def get_next_path(cls, last_path: str):
        last = list(last_path)
        mapping = list(map(lambda x: LETTERS.find(x), last))
        next_increment = True
        idx = cls.MAX_LETTER - 1
        while idx >= 0:
            if next_increment:
                if mapping[idx] + 1 == len(LETTERS):
                    mapping[idx] = 0
                    next_increment = True
                else:
                    mapping[idx] += 1
                    next_increment = False
            idx -= 1

        return "".join(map(lambda x: LETTERS[x], mapping))
