from django.db import models
from profile.models import MyUser,Skills


class CodeSubmission(models.Model):
    CONTENT_TYPES = [
        ('text', 'Text'),
        ('video', 'Video'),
        ('gist', 'Gist'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('locked', 'Locked'),
        ('completed', 'Completed'),
    ]
    user= models.ForeignKey(MyUser,related_name="user",on_delete=models.CASCADE)
    skill=models.ManyToManyField(Skills,related_name="code_skills")
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    session_type = models.CharField(max_length=10, choices=[('text', 'Text'), ('video', 'Video')])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    accepted_bid = models.OneToOneField('Bid', on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_submission')
    question=models.TextField()
    code=models.TextField(blank=True, null=True)
    gist_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Bid(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    reviewer = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='bids')
    submission = models.ForeignKey(CodeSubmission, on_delete=models.CASCADE, related_name='bids')
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    availability = models.DateTimeField()  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.reviewer.username} for {self.submission}"

    class Meta:
        ordering = ['created_at']
        
        
class Session(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    submission = models.ForeignKey(CodeSubmission, on_delete=models.CASCADE, related_name='sessions')
    reviewer = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='review_sessions')
    type = models.CharField(max_length=10, choices=[('text', 'Text'), ('video', 'Video')])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    disputed = models.BooleanField(default=False)  # Flags fraud complaints
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session for {self.submission} by {self.reviewer.username}"

    class Meta:
        ordering = ['created_at']

class Review(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name='review')
    text = models.TextField(blank=True)  # Text feedback
    video_url = models.URLField(max_length=500, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.session}"

    class Meta:
        ordering = ['created_at']
        
#payment ko kura haru last ma intergrarte garna xa