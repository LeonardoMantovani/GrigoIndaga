from django.contrib import admin
from .models import Classe, Professore, Votazione, Materia
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Your Model Resources (for import-export)
class RisorsaClasse(resources.ModelResource):

    class Meta:
        model = Classe
        exclude = ('id',)
        import_id_fields = ('nome',)


class RisorsaProfessore(resources.ModelResource):

    class Meta:
        model = Professore
        exclude = ('id',)
        import_id_fields = ('nome',)


# Your Resources Admins (for import-export)
class AdminClasse(ImportExportModelAdmin):
    resource_class = RisorsaClasse


class AdminProfessore(ImportExportModelAdmin):
    resource_class = RisorsaProfessore


# Register your models here.
admin.site.register(Classe, AdminClasse)
admin.site.register(Professore, AdminProfessore)
admin.site.register(Votazione)
admin.site.register(Materia)
