# Generated by Django 4.0.1 on 2022-02-14 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phone',
            options={'ordering': ['id'], 'verbose_name': 'Смартфоны', 'verbose_name_plural': 'Смартфоны'},
        ),
        migrations.AddField(
            model_name='phone',
            name='count',
            field=models.CharField(max_length=15, null=True, verbose_name='В налиичии'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='caption',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='Site.category', verbose_name='Бренд'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Публикация'),
        ),
    ]
