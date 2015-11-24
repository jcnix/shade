from django.db import models
from django_markdown.models import MarkdownField
from django.contrib.auth.models import User

class Language(models.Model):
    name = models.CharField(max_length=20)
    abbr = models.CharField(max_length=3)

    def __unicode__(self):
        return name

class Group(models.Model):
    class Meta:
        ordering = ['priority']

    name = models.CharField(max_length=150)
    priority = models.IntegerField(null=True, blank=True)
    members = models.ManyToManyField(User, blank=True)

    def __unicode__(self):
        return self.name

class Relationship(models.Model):
    name = models.CharField(max_length=25)
    has_partner = models.BooleanField()

    def __unicode__(self):
        return name

class SchoolLevel(models.Model):
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return name

class School(models.Model):
    name = models.CharField(max_length=100)
    level = models.ForeignKey(SchoolLevel)

    def __unicode__(self):
        return name

class SchoolMembership(models.Model):
    student = models.ForeignKey('UserProfile')
    school = models.ForeignKey(School)
    graduation = models.DateField()
    study = models.CharField(max_length=100)

class Employer(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return name

class EmployerMembership(models.Model):
    employee = models.ForeignKey('UserProfile')
    employer = models.ForeignKey(Employer)
    start_date = models.DateField()
    end_date = models.DateField()

class Message(models.Model):
    class Meta:
        get_latest_by = 'sent'
        ordering = ['-sent']

    author = models.ForeignKey(User, related_name='mfrom')
    recipient = models.ForeignKey(User, related_name='mto')
    subject = models.CharField(max_length=50)
    body = models.TextField()
    read = models.BooleanField()
    sent = models.DateTimeField()

    def __unicode__(self):
        return subject

class Comment(models.Model):
    class Meta:
        get_latest_by = 'sent'
        ordering = ['-sent']

    author = models.ForeignKey(User)
    post = models.CharField(max_length=500)
    read = models.BooleanField()
    sent = models.DateTimeField()
    public = models.BooleanField(default=False)
    subcomments = models.ManyToManyField('SubComment', blank=True)

class SubComment(Comment):
    parent = models.ForeignKey(Comment, related_name='parent')

class Picture(models.Model):
    image = models.ImageField(upload_to='uploads/')
    caption = models.CharField(max_length=140, blank=True)
    tagged = models.ManyToManyField(User, blank=True)
    uploaded = models.DateField()
    comments = models.ManyToManyField(Comment, blank=True)

class Album(models.Model):
    name = models.CharField(max_length=40)
    pictures = models.ManyToManyField('Picture', blank=True)

#Friend invite
class Invite(models.Model):
    user = models.ForeignKey(User)
    sender = models.ForeignKey(User, related_name='sender')
    sent = models.DateTimeField()

class EventInvite(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey('Event')
    sent = models.DateTimeField()

class Event(models.Model):
    class Meta:
        get_latest_by = 'datetime'
        ordering = ['-datetime']

    title = models.CharField(max_length=50)
    description = models.TextField()
    author = models.ForeignKey(User, related_name='author')
    attending = models.ManyToManyField(User, related_name='attnd')
    maybe = models.ManyToManyField(User, related_name='attnd_m')
    not_attending = models.ManyToManyField(User, related_name='attend_n')
    awaiting = models.ManyToManyField(User, related_name='await')
    datetime = models.DateTimeField()

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.ForeignKey(Picture, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    bio = MarkdownField(null=True, blank=True)
    gender = models.CharField(max_length=6, null=True, blank=True, choices=(("Male", "Male"), ("Female", "Female")))
    spoken_languages = models.CharField(max_length=150, null=True, blank=True)
    hometown = models.CharField(max_length=40, null=True, blank=True)
    home_country = models.CharField(max_length=25, null=True, blank=True)
    home_state = models.CharField(max_length=30, null=True, blank=True)
    current_town = models.CharField(max_length=40, null=True, blank=True)
    current_country = models.CharField(max_length=25, null=True, blank=True)
    current_state = models.CharField(max_length=30, null=True, blank=True)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    subscriptions = models.ManyToManyField(User, blank=True, related_name='subscriptions')
    invites = models.ManyToManyField(Invite, blank=True, related_name='invites')
    event_invites = models.ManyToManyField(EventInvite, blank=True, related_name='event_invites')
    albums = models.ManyToManyField(Album, blank=True)
    events = models.ManyToManyField(Event, blank=True)
    relationship_status = models.ForeignKey(Relationship, null=True, blank=True)
    schools = models.ManyToManyField(School, through=SchoolMembership, blank=True)
    employers = models.ManyToManyField(Employer, through=EmployerMembership, blank=True)
    messages = models.ManyToManyField(Message, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    site_language = models.ForeignKey(Language, null=True, blank=True)
    url = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

import util
def create_profile(sender, **kwargs):
    if kwargs.get('created', False):
        user = kwargs.get('instance')
        url = util.gen_url()
        UserProfile.objects.create(user=user, url=url)

from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)

