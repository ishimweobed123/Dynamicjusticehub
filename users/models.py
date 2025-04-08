from django.db import models

class Location(models.Model):
    LOCATION_TYPES = (
        ('COUNTRY', 'Country'),
        ('PROVINCE', 'Province'),
        ('DISTRICT', 'District'),
        ('SECTOR', 'Sector'),
        ('CELL', 'Cell')
    )
    
    location_id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=20, choices=LOCATION_TYPES)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.type})"

class User(models.Model):
    SEX_CHOICES = (
        ('M', 'Male'), 
        ('F', 'Female')
        )
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def get_parent_id(location_id):
    str_id = str(location_id)
    if location_id == 0:
        return None  # Country has no parent
    return int(str_id[:-2]) if len(str_id) > 2 else 0 # int(str_id[0]) # Modified for simplicity