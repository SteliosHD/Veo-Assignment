from django.db import models


class Node(models.Model):
    NODE_TYPE_CHOICES = [
        ('MANAGER', 'Manager'),
        ('DEVELOPER', 'Developer'),
        ('NONE', 'None')
    ]
    id = models.IntegerField(primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    parent_id = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    node_type = models.CharField(max_length=50, choices=NODE_TYPE_CHOICES, default='NONE')
    department_name = models.CharField(max_length=50, null=True, blank=True)
    language_preference = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.id, self.name, self.node_type)

    def save(self, *args, **kwargs):
        if self.parent_id is None:
            self.height = 0
        else:
            self.height = self.parent_id.height + 1
        super().save(*args, **kwargs)
