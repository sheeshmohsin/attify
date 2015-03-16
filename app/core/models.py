from django.db import models
from core.utils import get_upload_file_path, validate_file_extension
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class UploadApk(models.Model):
	apk = models.FileField(_('Upload a Apk file '),
						   upload_to=get_upload_file_path, 
						   validators=[validate_file_extension])

	class Meta:
		verbose_name_plural = 'UploadApk'

	def __unicode__(self):
		return self.id


