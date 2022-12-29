# Generated by Django 4.1.4 on 2022-12-29 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_category_description_alter_product_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='updated_on',
            new_name='modified_on',
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('color', 'color'), ('size', 'size')], max_length=50)),
                ('value', models.CharField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
        ),
    ]
