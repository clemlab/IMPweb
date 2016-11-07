from django.contrib import admin

from .models import UserProfile, Seq, Predictor, SeqPred

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Seq)
admin.site.register(Predictor)
admin.site.register(SeqPred)
