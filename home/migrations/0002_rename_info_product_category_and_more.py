# Generated by Django 4.1.12 on 2024-01-25 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='info',
            new_name='Category',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='Quantity',
        ),
        migrations.RemoveField(
            model_name='product',
            name='name',
        ),
        migrations.AddField(
            model_name='product',
            name='City',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='Country',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='Customer_ID',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='Customer_Name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='Discount',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='Order_Date',
            field=models.DateTimeField(null=True, verbose_name='Order Date'),
        ),
        migrations.AddField(
            model_name='product',
            name='Order_ID',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='Postal_Code',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='Product_ID',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='Product_Name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='Profit',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='Region',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='Row_ID',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='Sales',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='Segment',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='Ship_Date',
            field=models.DateTimeField(null=True, verbose_name='Ship Date'),
        ),
        migrations.AddField(
            model_name='product',
            name='Ship_Mode',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='State',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='Sub_Category',
            field=models.CharField(default='', max_length=100),
        ),
    ]
