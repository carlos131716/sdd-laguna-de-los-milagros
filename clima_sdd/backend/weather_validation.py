def validate_city(city):
    city = city.strip()
    if not city:
        return "", "Ingrese el nombre de una ciudad."
    if len(city) < 2 or len(city) > 100:
        return city, "Ingrese un nombre de ciudad válido."
    return city, None
