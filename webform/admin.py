from django.contrib import admin

from .models import JobEntry, SubmissionEntry, JobBatch

# Register your models here.
#admin.site.register(UserProfile)
#admin.site.register(Seq)
#admin.site.register(Predictor)
#admin.site.register(SeqPred)
admin.site.register(JobEntry)
admin.site.register(JobBatch)
admin.site.register(SubmissionEntry)


#UserProfile, Seq, Predictor, SeqPred,