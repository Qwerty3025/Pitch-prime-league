from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_disciplinerule_entertainmentfeature_rulecategory_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerLogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('category', models.CharField(choices=[('sponsor', 'Sponsor'), ('supplier', 'Supplier')], max_length=20)),
                ('logo', models.ImageField(upload_to='partner_logos/')),
                ('website', models.URLField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('sort_order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['sort_order', 'name']},
        ),
    ]
