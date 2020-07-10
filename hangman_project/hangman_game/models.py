from django.db import models


class WordBank(models.Model):
    word = models.CharField(max_length=200, unique=False)

    def __str__(self):
        return self.word

    objects = models.Manager()


class GameState(models.Model):
    game_status = models.SmallIntegerField()
    word_to_guess_id = models.ForeignKey(WordBank, on_delete=models.CASCADE)
    word_mask = models.CharField(max_length=200)

    def __str__(self):
        return self.game_status

    objects = models.Manager()
