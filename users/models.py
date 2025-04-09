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

    """
    Determines the parent ID of a given location based on the location ID structure.
    
    The location ID system follows this pattern:
    - Country: 0
    - Province: 1-5 (1 digit)
    - District: 11-57 (2 digits, first digit is province ID)
    - Sector: 1101-5715 (4 digits, first 2 digits are district ID)
    - Cell: 110101-571514 (6 digits, first 4 digits are sector ID)
    
    Examples:
        get_parent_id(0) -> None (Country has no parent)
        get_parent_id(1) -> 0 (Province 1's parent is Country 0)
        get_parent_id(11) -> 1 (District 11's parent is Province 1)
        get_parent_id(1101) -> 11 (Sector 1101's parent is District 11)
        get_parent_id(110101) -> 1101 (Cell 110101's parent is Sector 1101)
    
    Args:
        location_id (int): The ID of the location to find the parent for
        
    Returns:
        int or None: The parent location ID, or None if the location is the country
    """
    
    # Convert location_id to string for manipulation
    str_id = str(location_id)
    
    # Country (ID: 0) has no parent To return
    if location_id == 0:
        return None
    
    # For IDs with more than 2 digits (Sectors and Cells):
    # Remove the last 2 digits to get the parent ID
    # Example: 110101 -> 1101 (Cell -> Sector)
    # Example: 1101 -> 11 (Sector -> District)
    if len(str_id) > 2:
        return int(str_id[:-2])
    
    # For IDs with 2 digits or less (Provinces and Districts):
    # If it's a province (1 digit), return 0 (Country)
    # If it's a district (2 digits), return the first digit (Province)
    # Example: 1 -> 0 (Province -> Country)
    # Example: 11 -> 1 (District -> Province)
    return 0  # For provinces, return country ID (0)