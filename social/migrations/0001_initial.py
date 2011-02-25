# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Language'
        db.create_table('social_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('abbr', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('social', ['Language'])

        # Adding model 'Group'
        db.create_table('social_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('social', ['Group'])

        # Adding model 'Relationship'
        db.create_table('social_relationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('has_partner', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('social', ['Relationship'])

        # Adding model 'SchoolLevel'
        db.create_table('social_schoollevel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('social', ['SchoolLevel'])

        # Adding model 'School'
        db.create_table('social_school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.SchoolLevel'])),
        ))
        db.send_create_signal('social', ['School'])

        # Adding model 'SchoolMembership'
        db.create_table('social_schoolmembership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.UserProfile'])),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.School'])),
            ('graduation', self.gf('django.db.models.fields.DateField')()),
            ('study', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('social', ['SchoolMembership'])

        # Adding model 'Employer'
        db.create_table('social_employer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('social', ['Employer'])

        # Adding model 'EmployerMembership'
        db.create_table('social_employermembership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.UserProfile'])),
            ('employer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.Employer'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('social', ['EmployerMembership'])

        # Adding model 'Message'
        db.create_table('social_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='from', to=orm['auth.User'])),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to', to=orm['auth.User'])),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sent', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('social', ['Message'])

        # Adding model 'Comment'
        db.create_table('social_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('post', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sent', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('social', ['Comment'])

        # Adding M2M table for field subcomments on 'Comment'
        db.create_table('social_comment_subcomments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comment', models.ForeignKey(orm['social.comment'], null=False)),
            ('subcomment', models.ForeignKey(orm['social.subcomment'], null=False))
        ))
        db.create_unique('social_comment_subcomments', ['comment_id', 'subcomment_id'])

        # Adding model 'SubComment'
        db.create_table('social_subcomment', (
            ('comment_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['social.Comment'], unique=True, primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parent', to=orm['social.Comment'])),
        ))
        db.send_create_signal('social', ['SubComment'])

        # Adding model 'Picture'
        db.create_table('social_picture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=140, null=True, blank=True)),
            ('uploaded', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('social', ['Picture'])

        # Adding M2M table for field tagged on 'Picture'
        db.create_table('social_picture_tagged', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('picture', models.ForeignKey(orm['social.picture'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('social_picture_tagged', ['picture_id', 'user_id'])

        # Adding M2M table for field comments on 'Picture'
        db.create_table('social_picture_comments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('picture', models.ForeignKey(orm['social.picture'], null=False)),
            ('comment', models.ForeignKey(orm['social.comment'], null=False))
        ))
        db.create_unique('social_picture_comments', ['picture_id', 'comment_id'])

        # Adding model 'Album'
        db.create_table('social_album', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('social', ['Album'])

        # Adding M2M table for field pictures on 'Album'
        db.create_table('social_album_pictures', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('album', models.ForeignKey(orm['social.album'], null=False)),
            ('picture', models.ForeignKey(orm['social.picture'], null=False))
        ))
        db.create_unique('social_album_pictures', ['album_id', 'picture_id'])

        # Adding model 'Invite'
        db.create_table('social_invite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sender', to=orm['auth.User'])),
            ('sent', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('social', ['Invite'])

        # Adding model 'EventInvite'
        db.create_table('social_eventinvite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.Event'])),
            ('sent', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('social', ['EventInvite'])

        # Adding model 'Event'
        db.create_table('social_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='author', to=orm['auth.User'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('social', ['Event'])

        # Adding M2M table for field attending on 'Event'
        db.create_table('social_event_attending', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['social.event'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('social_event_attending', ['event_id', 'user_id'])

        # Adding M2M table for field maybe on 'Event'
        db.create_table('social_event_maybe', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['social.event'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('social_event_maybe', ['event_id', 'user_id'])

        # Adding M2M table for field not_attending on 'Event'
        db.create_table('social_event_not_attending', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['social.event'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('social_event_not_attending', ['event_id', 'user_id'])

        # Adding M2M table for field awaiting on 'Event'
        db.create_table('social_event_awaiting', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['social.event'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('social_event_awaiting', ['event_id', 'user_id'])

        # Adding model 'UserProfile'
        db.create_table('social_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('profile_picture', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.Picture'], null=True, blank=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('spoken_languages', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('hometown', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('home_country', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('home_state', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('current_town', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('current_country', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('current_state', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('relationship_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.Relationship'], null=True, blank=True)),
            ('site_language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social.Language'], null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal('social', ['UserProfile'])

        # Adding M2M table for field friends on 'UserProfile'
        db.create_table('social_userprofile_friends', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['social.userprofile'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('social_userprofile_friends', ['userprofile_id', 'user_id'])

        # Adding M2M table for field invites on 'UserProfile'
        db.create_table('social_userprofile_invites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['social.userprofile'], null=False)),
            ('invite', models.ForeignKey(orm['social.invite'], null=False))
        ))
        db.create_unique('social_userprofile_invites', ['userprofile_id', 'invite_id'])

        # Adding M2M table for field event_invites on 'UserProfile'
        db.create_table('social_userprofile_event_invites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['social.userprofile'], null=False)),
            ('eventinvite', models.ForeignKey(orm['social.eventinvite'], null=False))
        ))
        db.create_unique('social_userprofile_event_invites', ['userprofile_id', 'eventinvite_id'])

        # Adding M2M table for field albums on 'UserProfile'
        db.create_table('social_userprofile_albums', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['social.userprofile'], null=False)),
            ('album', models.ForeignKey(orm['social.album'], null=False))
        ))
        db.create_unique('social_userprofile_albums', ['userprofile_id', 'album_id'])

        # Adding M2M table for field events on 'UserProfile'
        db.create_table('social_userprofile_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['social.userprofile'], null=False)),
            ('event', models.ForeignKey(orm['social.event'], null=False))
        ))
        db.create_unique('social_userprofile_events', ['userprofile_id', 'event_id'])

        # Adding M2M table for field messages on 'UserProfile'
        db.create_table('social_userprofile_messages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['social.userprofile'], null=False)),
            ('message', models.ForeignKey(orm['social.message'], null=False))
        ))
        db.create_unique('social_userprofile_messages', ['userprofile_id', 'message_id'])

        # Adding M2M table for field comments on 'UserProfile'
        db.create_table('social_userprofile_comments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['social.userprofile'], null=False)),
            ('comment', models.ForeignKey(orm['social.comment'], null=False))
        ))
        db.create_unique('social_userprofile_comments', ['userprofile_id', 'comment_id'])


    def backwards(self, orm):
        
        # Deleting model 'Language'
        db.delete_table('social_language')

        # Deleting model 'Group'
        db.delete_table('social_group')

        # Deleting model 'Relationship'
        db.delete_table('social_relationship')

        # Deleting model 'SchoolLevel'
        db.delete_table('social_schoollevel')

        # Deleting model 'School'
        db.delete_table('social_school')

        # Deleting model 'SchoolMembership'
        db.delete_table('social_schoolmembership')

        # Deleting model 'Employer'
        db.delete_table('social_employer')

        # Deleting model 'EmployerMembership'
        db.delete_table('social_employermembership')

        # Deleting model 'Message'
        db.delete_table('social_message')

        # Deleting model 'Comment'
        db.delete_table('social_comment')

        # Removing M2M table for field subcomments on 'Comment'
        db.delete_table('social_comment_subcomments')

        # Deleting model 'SubComment'
        db.delete_table('social_subcomment')

        # Deleting model 'Picture'
        db.delete_table('social_picture')

        # Removing M2M table for field tagged on 'Picture'
        db.delete_table('social_picture_tagged')

        # Removing M2M table for field comments on 'Picture'
        db.delete_table('social_picture_comments')

        # Deleting model 'Album'
        db.delete_table('social_album')

        # Removing M2M table for field pictures on 'Album'
        db.delete_table('social_album_pictures')

        # Deleting model 'Invite'
        db.delete_table('social_invite')

        # Deleting model 'EventInvite'
        db.delete_table('social_eventinvite')

        # Deleting model 'Event'
        db.delete_table('social_event')

        # Removing M2M table for field attending on 'Event'
        db.delete_table('social_event_attending')

        # Removing M2M table for field maybe on 'Event'
        db.delete_table('social_event_maybe')

        # Removing M2M table for field not_attending on 'Event'
        db.delete_table('social_event_not_attending')

        # Removing M2M table for field awaiting on 'Event'
        db.delete_table('social_event_awaiting')

        # Deleting model 'UserProfile'
        db.delete_table('social_userprofile')

        # Removing M2M table for field friends on 'UserProfile'
        db.delete_table('social_userprofile_friends')

        # Removing M2M table for field invites on 'UserProfile'
        db.delete_table('social_userprofile_invites')

        # Removing M2M table for field event_invites on 'UserProfile'
        db.delete_table('social_userprofile_event_invites')

        # Removing M2M table for field albums on 'UserProfile'
        db.delete_table('social_userprofile_albums')

        # Removing M2M table for field events on 'UserProfile'
        db.delete_table('social_userprofile_events')

        # Removing M2M table for field messages on 'UserProfile'
        db.delete_table('social_userprofile_messages')

        # Removing M2M table for field comments on 'UserProfile'
        db.delete_table('social_userprofile_comments')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'social.album': {
            'Meta': {'object_name': 'Album'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'pictures': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social.Picture']", 'null': 'True', 'blank': 'True'})
        },
        'social.comment': {
            'Meta': {'ordering': "['-sent']", 'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {}),
            'subcomments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social.SubComment']", 'null': 'True', 'blank': 'True'})
        },
        'social.employer': {
            'Meta': {'object_name': 'Employer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'social.employermembership': {
            'Meta': {'object_name': 'EmployerMembership'},
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social.UserProfile']"}),
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social.Employer']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'social.event': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Event'},
            'attending': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'attnd'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'author'", 'to': "orm['auth.User']"}),
            'awaiting': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'await'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maybe': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'attnd_m'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'not_attending': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'attend_n'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'social.eventinvite': {
            'Meta': {'object_name': 'EventInvite'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'social.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'social.invite': {
            'Meta': {'object_name': 'Invite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sender'", 'to': "orm['auth.User']"}),
            'sent': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'social.language': {
            'Meta': {'object_name': 'Language'},
            'abbr': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'social.message': {
            'Meta': {'ordering': "['-sent']", 'object_name': 'Message'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from'", 'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to'", 'to': "orm['auth.User']"}),
            'sent': ('django.db.models.fields.DateTimeField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'social.picture': {
            'Meta': {'object_name': 'Picture'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '140', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social.Comment']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'tagged': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'uploaded': ('django.db.models.fields.DateField', [], {})
        },
        'social.relationship': {
            'Meta': {'object_name': 'Relationship'},
            'has_partner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'social.school': {
            'Meta': {'object_name': 'School'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social.SchoolLevel']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'social.schoollevel': {
            'Meta': {'object_name': 'SchoolLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'social.schoolmembership': {
            'Meta': {'object_name': 'SchoolMembership'},
            'graduation': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social.School']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social.UserProfile']"}),
            'study': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'social.subcomment': {
            'Meta': {'ordering': "['-sent']", 'object_name': 'SubComment', '_ormbases': ['social.Comment']},
            'comment_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['social.Comment']", 'unique': 'True', 'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parent'", 'to': "orm['social.Comment']"})
        },
        'social.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social.Album']", 'null': 'True', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social.Comment']", 'null': 'True', 'blank': 'True'}),
            'current_country': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'current_state': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'current_town': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'employers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social.Employer']", 'null': 'True', 'through': "orm['social.EmployerMembership']", 'blank': 'True'}),
            'event_invites': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'event_invites'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['social.EventInvite']"}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social.Event']", 'null': 'True', 'blank': 'True'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'friends'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'home_country': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'home_state': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'hometown': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invites': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'invites'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['social.Invite']"}),
            'messages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social.Message']", 'null': 'True', 'blank': 'True'}),
            'profile_picture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social.Picture']", 'null': 'True', 'blank': 'True'}),
            'relationship_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social.Relationship']", 'null': 'True', 'blank': 'True'}),
            'schools': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['social.School']", 'null': 'True', 'through': "orm['social.SchoolMembership']", 'blank': 'True'}),
            'site_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['social.Language']", 'null': 'True', 'blank': 'True'}),
            'spoken_languages': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['social']
