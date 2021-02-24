from django.contrib import admin
from django.contrib.admin.decorators import register
from django.utils.safestring import mark_safe

from clientes.models import DatoFacturacion, Cliente


class DatoFacturacionInline(admin.TabularInline):
    model = DatoFacturacion
    extra = 0


@register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields = ('nombre', )
    list_display = ('editar', 'ver', 'nombre', 'documento', 'telefono', 'get_profesional_responsable')
    inlines = (DatoFacturacionInline, )
    actions = None
    fieldsets = (
        (None, {
            'fields': [
                'nombre',
                'documento',
                'telefono',
                'direccion',
                'email',
                'nacimiento',
            ]
        }),
        (None, {
            'fields': [
                'parto',
                'antibioticos_en_infancia'
            ]
        }),
        ('COMORBILIDADES', {
            'fields': [
                'hipertension_arterial',
                'diabetes_mellitus_tipo_2',
                'dislipidemia',
                'hipotiroidismo',
                'hipertiroidismo',
                'tiroiditis',
                'rinitis_alergica',
                'asma',
                'gastritis',
                'sindrome_del_intestino_irritable',
                'celiaquia',
                'transtorno_de_ansiedad',
                'sindrome_de_panico',
                'depresion',
                'anemia',
                'sindrome_de_ovario_poliquistico',
                'otras_comorbolidades'
            ]
        }),
        ('Cirugías', {
            'fields': [
                'adenoides',
                'amigdalectomia',
                'apendicectomia',
                'histerectomia',
                'hemorroides',
                'colecistectomia',
                'otras_cirugias'
            ]
        }),
        ('Medicamentos', {
            'fields': [
                'antibioticos',
                'corticoides',
                'antidepresivos',
                'anticonceptivos',
                'inhibidor_de_bomba_de_protones',
                'metformina',
                'quimioterapia',
                'analgesicos',
                'otros_medicamentos'
            ]
        }),
        ('Sistema Nervioso', {
            'fields': [
                'cefalea',
                'cansancio_o_fatiga',
                'insomnio',
                'se_despierta_por_las_noches',
                'bruxismo',
                'perdida_de_memoria',
                'falta_de_concentracion',
                'mareos',
                'irritabilidad',
                'ansiedad',
                'abombamiento'
            ]
        }),
        ('Aparato Respiratorio', {
            'fields': [
                'congestion_nasal',
                'estornudos',
                'tos_cronica',
                'sibilancias',
                'frecuente_sensacion_de_limpiar_la_garganta'
            ]
        }),
        ('Aparato Circulatorio', {
            'fields': [
                'retencion_de_liquidos',
                'palpitaciones',
                'varices',
                'manos_y_pies_frias',
            ]
        }),
        ('Aparato Digestivo', {
            'fields': [
                'aftas_en_la_boca',
                'halitosis',
                'acides_estomacal',
                'nauseas',
                'vomitos',
                'dolor_abdominal',
                'distencion_abdominal',
                'reflujo',
                'diarreas',
                'estrenimiento'
            ]
        }),
        (None, {
            'fields': [
                'va_de_cuerpo_cada',
                'forma_de_materia_fecal'
            ]
        }),
        ('Aparato Tegumentario', {
            'fields': [
                'alergias_en_el_rostro',
                'alergias_en_la_piel'
            ]
        }),
        ('Aparato Ostomuscular', {
            'fields': [
                'dolor_articular',
            ]
        }),
        (None, {
            'fields': [
                'bio_resonancia_cuantica',
            ]
        }),
    )

    def editar(self, obj):
        html = '<a href="/admin/clientes/cliente/%s" class="icon-block"> <i class="fa fa-edit"></i></a>' % obj.pk
        return mark_safe(html)

    def ver(self, obj):
        html = '<a href="/admin/clientes/cliente_detail/%s" class="icon-block"> <i class="fa fa-eye"></i></a>' % obj.pk
        return mark_safe(html)