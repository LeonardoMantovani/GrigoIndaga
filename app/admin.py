from django.contrib import admin
from .models import Classe
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Your Model Resources (for import-export)
class RisorsaClasse(resources.ModelResource):

    class Meta:
        model = Classe
        exclude = ('id',)
        import_id_fields = ('nome',)


# Your Resources Admins (for import-export)
class AdminClasse(ImportExportModelAdmin):
    resource_class = RisorsaClasse


# Register your models here.
admin.site.register(Classe, AdminClasse)