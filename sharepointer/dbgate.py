#/usr/bin/python2

from django.contrib.auth.models import User
from django.http import HttpResponse


import threading
import models
import jobs


class NotificationEntity(dict):
	def __init__(self, notif):
		self['notification_id'] = notif.pk
		self['message'] = notif.message
		if notif.file:
			self['filename'] = notif.file.file_name
			self['date'] = notif.file.upload_date.ctime()
			self['fileid'] = notif.file.pk

	def __getattr__(self, key):
		return self[key]

	def __repr__(self):     
		return '<NotificationEntity @ %s>' % str(hex(id(self)))


def upload_file(user, to, filename, content):
	emails = []
	if to == 'all':
		emails = [str(obj.email) for obj in User.objects.all()]
		emails.remove(user.email)
	file_entity = models.CentralFileStore(file_name=filename, file_content=content, owner=user)
	if emails:
		file_entity.set_recipients(emails)
	else:
		file_entity.set_recipients([to])
	file_entity.save()
	sent_entity = models.SentFiles(user=user, file=file_entity)
	sent_entity.save()
	return file_entity, sent_entity


def get_all_files():
	return models.CentralFileStore.objects.all()


def get_all_edited_files():
	return models.EditedFiles.objects.all()

def get_all_received_files(user):
	files = models.CentralFileStore.objects.all()
	results = []
	for file in files:
		recepients = file.get_recipients()
		if str(user.email) in recepients:
			results.append(file)
	return results


def get_all_sent_files(user):
	return user.sentfiles_set.all()


def delete_file(oid, section):
	oid = int(oid)
	
	if section == "received":
		file = models.CentralFileStore.objects.get(pk=oid)
		filename = file.file_name
		file.delete()
	elif section == "sent":
		sent = models.SentFiles.objects.get(pk=oid)
		file = sent.file
		filename = file.file_name
		sent.delete()
		file.delete()
	else:
		file = models.EditedFiles.objects.get(pk=oid)
		file.delete()
	return filename


def download_file(oid, section):
	oid = int(oid)
	if section == "received":
		file = models.CentralFileStore.objects.get(pk=oid)
		response = HttpResponse(file.file_content)
		response['Content-Disposition'] = 'attachment; filename=%s' % file.file_name
		return response
	elif section == "sent":
		file = models.SentFiles.objects.get(pk=oid).file
		response = HttpResponse(file.file_content)
		response['Content-Disposition'] = 'attachment; filename=%s' % file.file_name
		return response
	else:
		file = models.EditedFiles.objects.get(pk=oid)
		response = HttpResponse(file.file_content)
		response['Content-Disposition'] = 'attachment; filename=%s' % file.file_name
		return response


def update_file(uid, content):
	file = models.CentralFileStore.objects.get(pk=uid)
	if str(file.file_content) == content:
		return file
	file.file_content = content
	file.updated = True
	file.save()
	return file


def hard_file_update(uid, content, user, lobby=None):
	if lobby:
		original_file = models.EditedFiles.objects.get(pk=uid)
	else:
		original_file = models.CentralFileStore.objects.get(pk=uid)
	if str(original_file.file_content) == content:
		return original_file
	edit_record = models.EditedFiles(edited_by=user, file_content=content, file_name=original_file.file_name)
	edit_record.save()
	return edit_record


def add_notification(file, message):
	if file is None:
		notif = models.Notifications(message=message)
	else:
		notif = models.Notifications(message=message, file=file)
	notif.save()
	timer = threading.Timer(15, lambda entity: entity.delete(), (notif,))
	timer.start()
	return notif


def get_notifications():
	notif = models.Notifications.objects.all()
	return notif


def read_notifications():
	notifs = get_notifications()
	_notifs = []
	for notif in notifs:
		_notifs.append(NotificationEntity(notif))
	return _notifs


def is_there_notifications():
	notifs = get_notifications()
	return (notifs.count() > 0)
