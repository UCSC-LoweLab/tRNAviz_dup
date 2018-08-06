# Generated by Django 2.0.6 on 2018-08-06 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0015_auto_20180806_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trna',
            name='isotype',
            field=models.CharField(choices=[('Ala', 'Ala'), ('Arg', 'Arg'), ('Asn', 'Asn'), ('Asp', 'Asp'), ('Cys', 'Cys'), ('Gln', 'Gln'), ('Glu', 'Glu'), ('Gly', 'Gly'), ('His', 'His'), ('Ile', 'Ile'), ('iMet', 'iMet'), ('Leu', 'Leu'), ('Lys', 'Lys'), ('Met', 'Met'), ('Phe', 'Phe'), ('Pro', 'Pro'), ('Ser', 'Ser'), ('SeC', 'SeC'), ('Thr', 'Thr'), ('Trp', 'Trp'), ('Tyr', 'Tyr'), ('Und', 'Und'), ('Val', 'Val')], max_length=5),
        ),
    ]
