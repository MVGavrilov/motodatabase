from django.http import HttpResponse, JsonResponse

from assortment.models import Model, Manufacturer


def get_models(request, manufacturer_id):
    models = Model.objects.filter(manufacturer_id=manufacturer_id)
    id_models = []
    for model in models:
        id_models.append({"id": model.id, "name": model.name})
    return JsonResponse(id_models, safe=False)


def get_manufacturers(request):
    manufacturers = Manufacturer.objects.all()
    id_manufacturers = []
    for manufacturer in manufacturers:
        id_manufacturers.append({"id": manufacturer.id, "name": manufacturer.name})
    return JsonResponse(id_manufacturers, safe=False)
