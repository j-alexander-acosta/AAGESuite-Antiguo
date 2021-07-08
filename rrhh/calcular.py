from django.db import models
from datetime import timedelta
from datetime import date

def sumar_dias_mas_fecha(dias, fecha):
    try:
        date = datetime.strptime(fecha, "%Y/%m/%d")
        modified_date = date + timedelta(days=dias)
        return modified_date
    except error:
        return 0;
