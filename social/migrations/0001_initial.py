# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post', models.CharField(max_length=500)),
                ('read', models.BooleanField()),
                ('sent', models.DateTimeField()),
                ('public', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-sent'],
                'get_latest_by': 'sent',
            },
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EmployerMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('datetime', models.DateTimeField()),
                ('attending', models.ManyToManyField(related_name='attnd', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(related_name='author', to=settings.AUTH_USER_MODEL)),
                ('awaiting', models.ManyToManyField(related_name='await', to=settings.AUTH_USER_MODEL)),
                ('maybe', models.ManyToManyField(related_name='attnd_m', to=settings.AUTH_USER_MODEL)),
                ('not_attending', models.ManyToManyField(related_name='attend_n', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datetime'],
                'get_latest_by': 'datetime',
            },
        ),
        migrations.CreateModel(
            name='EventInvite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent', models.DateTimeField()),
                ('event', models.ForeignKey(to='social.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('priority', models.IntegerField(null=True, blank=True)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent', models.DateTimeField()),
                ('sender', models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('abbr', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('read', models.BooleanField()),
                ('sent', models.DateTimeField()),
                ('author', models.ForeignKey(related_name='mfrom', to=settings.AUTH_USER_MODEL)),
                ('recipient', models.ForeignKey(related_name='mto', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sent'],
                'get_latest_by': 'sent',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'uploads/')),
                ('caption', models.CharField(max_length=140, blank=True)),
                ('uploaded', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
                ('has_partner', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('graduation', models.DateField()),
                ('study', models.CharField(max_length=100)),
                ('school', models.ForeignKey(to='social.School')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birthdate', models.DateField(null=True, blank=True)),
                ('bio', models.TextField(null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=6, null=True, choices=[(b'Male', b'Male'), (b'Female', b'Female')])),
                ('spoken_languages', models.CharField(max_length=150, null=True, blank=True)),
                ('hometown', models.CharField(max_length=40, null=True, blank=True)),
                ('home_country', models.CharField(max_length=25, null=True, blank=True)),
                ('home_state', models.CharField(max_length=30, null=True, blank=True)),
                ('current_town', models.CharField(max_length=40, null=True, blank=True)),
                ('current_country', models.CharField(max_length=25, null=True, blank=True)),
                ('current_state', models.CharField(max_length=30, null=True, blank=True)),
                ('url', models.CharField(unique=True, max_length=20)),
                ('albums', models.ManyToManyField(to='social.Album', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubComment',
            fields=[
                ('comment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='social.Comment')),
            ],
            bases=('social.comment',),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='comments',
            field=models.ManyToManyField(to='social.Comment', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='employers',
            field=models.ManyToManyField(to='social.Employer', through='social.EmployerMembership', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='event_invites',
            field=models.ManyToManyField(related_name='event_invites', to='social.EventInvite', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='events',
            field=models.ManyToManyField(to='social.Event', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(related_name='friends', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(to='social.Group', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='invites',
            field=models.ManyToManyField(related_name='invites', to='social.Invite', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='messages',
            field=models.ManyToManyField(to='social.Message', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ForeignKey(blank=True, to='social.Picture', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='relationship_status',
            field=models.ForeignKey(blank=True, to='social.Relationship', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='schools',
            field=models.ManyToManyField(to='social.School', through='social.SchoolMembership', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='site_language',
            field=models.ForeignKey(blank=True, to='social.Language', null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='subscriptions',
            field=models.ManyToManyField(related_name='subscriptions', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='schoolmembership',
            name='student',
            field=models.ForeignKey(to='social.UserProfile'),
        ),
        migrations.AddField(
            model_name='school',
            name='level',
            field=models.ForeignKey(to='social.SchoolLevel'),
        ),
        migrations.AddField(
            model_name='picture',
            name='comments',
            field=models.ManyToManyField(to='social.Comment', blank=True),
        ),
        migrations.AddField(
            model_name='picture',
            name='tagged',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='employermembership',
            name='employee',
            field=models.ForeignKey(to='social.UserProfile'),
        ),
        migrations.AddField(
            model_name='employermembership',
            name='employer',
            field=models.ForeignKey(to='social.Employer'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='album',
            name='pictures',
            field=models.ManyToManyField(to='social.Picture', blank=True),
        ),
        migrations.AddField(
            model_name='subcomment',
            name='parent',
            field=models.ForeignKey(related_name='parent', to='social.Comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='subcomments',
            field=models.ManyToManyField(to='social.SubComment', blank=True),
        ),
    ]
