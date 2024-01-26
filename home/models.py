from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

class Product(models.Model):
    id    = models.AutoField(primary_key=True)
    Row_ID = models.IntegerField(blank=True, null=True)
    Order_ID = models.CharField(max_length = 100, default = '')
    Order_Date = models.CharField(max_length = 10, null=True)
    Ship_Date = models.CharField(max_length = 10, null=True)
    Ship_Mode = models.CharField(max_length = 100, default = '')
    Customer_ID = models.CharField(max_length = 100, default = '')
    Customer_Name = models.CharField(max_length = 100, default = '')
    Segment = models.CharField(max_length = 100, default = '')
    Country = models.CharField(max_length = 100, default = '')
    City = models.CharField(max_length = 100, default = '')
    State = models.CharField(max_length = 100, default = '')
    Postal_Code = models.CharField(max_length = 100, default = '')
    Region = models.CharField(max_length = 100, default = '')
    Product_ID = models.CharField(max_length = 100, default = '')
    Category = models.CharField(max_length = 100, default = '')
    Sub_Category = models.CharField(max_length = 100, default = '')
    Product_Name = models.CharField(max_length = 100, default = '')
    Sales = models.CharField(max_length = 100, default = '')
    Quantity = models.IntegerField(blank=True, null=True)
    Discount = models.CharField(max_length = 100, default = '')
    Profit = models.CharField(max_length = 100, default = '')

    def __str__(self):
        return self.Product_Name
   