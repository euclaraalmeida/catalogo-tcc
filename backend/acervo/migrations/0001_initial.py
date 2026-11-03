import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='e-mail')),
            ],
            options={
                'verbose_name': 'autor',
                'verbose_name_plural': 'autores',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('sigla', models.CharField(max_length=15, unique=True)),
            ],
            options={
                'verbose_name': 'curso',
                'verbose_name_plural': 'cursos',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Orientador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('titulacao', models.CharField(max_length=100, verbose_name='titulação')),
                ('email_institucional', models.EmailField(max_length=254, unique=True, verbose_name='e-mail institucional')),
            ],
            options={
                'verbose_name': 'orientador',
                'verbose_name_plural': 'orientadores',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='PalavraChave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('termo', models.CharField(max_length=60, unique=True)),
            ],
            options={
                'verbose_name': 'palavra-chave',
                'verbose_name_plural': 'palavras-chave',
                'ordering': ['termo'],
            },
        ),
        migrations.CreateModel(
            name='Trabalho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=250, verbose_name='título')),
                ('resumo', models.TextField()),
                ('ano', models.PositiveSmallIntegerField()),
                ('data_defesa', models.DateField(blank=True, null=True, verbose_name='data da defesa')),
                ('nota', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('situacao', models.CharField(choices=[('EA', 'Em andamento'), ('DE', 'Defendido'), ('PU', 'Publicado')], default='EA', max_length=2, verbose_name='situação')),
                ('link_pdf', models.URLField(blank=True, verbose_name='link do PDF')),
                ('autores', models.ManyToManyField(related_name='trabalhos', to='acervo.autor')),
                ('cadastrado_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='trabalhos_cadastrados', to=settings.AUTH_USER_MODEL)),
                ('coorientador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trabalhos_coorientados', to='acervo.orientador')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='trabalhos', to='acervo.curso')),
                ('orientador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='trabalhos_orientados', to='acervo.orientador')),
                ('palavras_chave', models.ManyToManyField(related_name='trabalhos', to='acervo.palavrachave')),
            ],
            options={
                'verbose_name': 'trabalho',
                'verbose_name_plural': 'trabalhos',
                'ordering': ['-ano', 'titulo', 'pk'],
            },
        ),
    ]
