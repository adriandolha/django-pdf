from django.db import models


class Report(models.Model):
    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ('view_report', 'View report'),
            ('create_report_pdf', 'Generate report PDF')
        )


class UserData(models.Model):
    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ('create_user_data', 'Create user data'),
        )
