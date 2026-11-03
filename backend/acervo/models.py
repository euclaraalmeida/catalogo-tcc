from django.conf import settings
from django.db import models


class Curso(models.Model):
    nome = models.CharField(max_length=150)
    sigla = models.CharField(max_length=15, unique=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'curso'
        verbose_name_plural = 'cursos'

    def __str__(self):
        return self.nome


class Orientador(models.Model):
    nome = models.CharField(max_length=150)
    titulacao = models.CharField('titulação', max_length=100)
    email_institucional = models.EmailField('e-mail institucional', unique=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'orientador'
        verbose_name_plural = 'orientadores'

    def __str__(self):
        return self.nome


class Autor(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField('e-mail', unique=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'autor'
        verbose_name_plural = 'autores'

    def __str__(self):
        return self.nome


class PalavraChave(models.Model):
    termo = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ['termo']
        verbose_name = 'palavra-chave'
        verbose_name_plural = 'palavras-chave'

    def __str__(self):
        return self.termo


class Trabalho(models.Model):
    class Situacao(models.TextChoices):
        EM_ANDAMENTO = 'EA', 'Em andamento'
        DEFENDIDO = 'DE', 'Defendido'
        PUBLICADO = 'PU', 'Publicado'

    titulo = models.CharField('título', max_length=250)
    resumo = models.TextField()
    ano = models.PositiveSmallIntegerField()
    data_defesa = models.DateField('data da defesa', blank=True, null=True)
    nota = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    situacao = models.CharField('situação', max_length=2, choices=Situacao.choices, default=Situacao.EM_ANDAMENTO)
    link_pdf = models.URLField('link do PDF', blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, related_name='trabalhos')
    orientador = models.ForeignKey(Orientador, on_delete=models.PROTECT, related_name='trabalhos_orientados')
    coorientador = models.ForeignKey(Orientador, on_delete=models.PROTECT, related_name='trabalhos_coorientados', blank=True, null=True)
    autores = models.ManyToManyField(Autor, related_name='trabalhos')
    palavras_chave = models.ManyToManyField(PalavraChave, related_name='trabalhos')
    cadastrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='trabalhos_cadastrados')

    class Meta:
        ordering = ['-ano', 'titulo', 'pk']
        verbose_name = 'trabalho'
        verbose_name_plural = 'trabalhos'

    def __str__(self):
        return self.titulo
