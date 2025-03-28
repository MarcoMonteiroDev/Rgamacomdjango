# Generated by Django 5.1.7 on 2025-03-28 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_produto_descricao'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='medida',
            field=models.CharField(choices=[('metros quadrados', 'M²'), ('metros', 'M'), ('milimetros', 'MM'), ('centimetros', 'C'), ('litros', 'L')], default='metros', max_length=20, verbose_name='Medida'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='categoria',
            field=models.CharField(choices=[('materiais de construcao', 'Materiais de Construção'), ('tintas e acessorios', 'Tintas e Acessorios'), ('pisos e revestimentos', 'Pisos e Revestimentos'), ('eletrico e acabamento', 'Eletrico e Acabamento')], default='materiais de construcao', max_length=40, verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='nome',
            field=models.CharField(max_length=80, verbose_name='Nome'),
        ),
    ]
