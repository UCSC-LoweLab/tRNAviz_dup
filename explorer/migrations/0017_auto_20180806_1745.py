# Generated by Django 2.0.6 on 2018-08-06 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explorer', '0016_auto_20180806_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trna',
            name='best_model',
            field=models.CharField(choices=[('Ala', 'Ala'), ('Arg', 'Arg'), ('Asn', 'Asn'), ('Asp', 'Asp'), ('Cys', 'Cys'), ('Gln', 'Gln'), ('Glu', 'Glu'), ('Gly', 'Gly'), ('His', 'His'), ('Ile', 'Ile'), ('iMet', 'iMet'), ('Leu', 'Leu'), ('Lys', 'Lys'), ('Met', 'Met'), ('Phe', 'Phe'), ('Pro', 'Pro'), ('Ser', 'Ser'), ('SeC', 'SeC'), ('Thr', 'Thr'), ('Trp', 'Trp'), ('Tyr', 'Tyr'), ('Und', 'Und'), ('Val', 'Val')], max_length=4),
        ),
    ]
