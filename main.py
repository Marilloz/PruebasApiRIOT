import requests

def load_api_key(file_path="key"):
    try:
        with open(file_path, "r") as file:
            api_key = file.readline().strip()  # Leer la primera línea y eliminar espacios en blanco
        return api_key
    except FileNotFoundError:
        raise Exception(f"No se encontró el archivo {file_path}. Asegúrate de que existe y contiene la clave de API.")

# Cargar la clave desde el archivo
API_KEY = load_api_key()
print(API_KEY)

# Función para obtener el ID de un invocador a partir de su nombre
def get_summoner_id(summoner_name, region):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    response = requests.get(url, headers={"X-Riot-Token": API_KEY})

    if response.status_code == 200:
        return response.json()['id']
    else:
        raise Exception(f"Error al obtener el ID del invocador: {response.status_code}")


# Función para obtener el historial de partidas del invocador
def get_match_history(summoner_id, region, count=20):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{summoner_id}/ids?start=0&count={count}"
    response = requests.get(url, headers={"X-Riot-Token": API_KEY})

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al obtener el historial de partidas: {response.status_code}")


# Función para obtener los detalles de una partida específica
def get_match_duration(match_id, region):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers={"X-Riot-Token": API_KEY})

    if response.status_code == 200:
        return response.json()['info']['gameDuration'] / 60  # convertir segundos a minutos
    else:
        raise Exception(f"Error al obtener detalles de la partida: {response.status_code}")


# Función para calcular las horas totales jugadas en el historial
def calculate_total_hours(summoner_name, region, match_count=20):
    summoner_id = get_summoner_id(summoner_name, region)
    match_history = get_match_history(summoner_id, region, match_count)

    total_duration = 0
    for match_id in match_history:
        match_duration = get_match_duration(match_id, region)
        total_duration += match_duration

    return total_duration / 60  # convertir minutos a horas


# Ejemplo de uso
summoner_name1 = "MÅRlLLΩZ#BAGHE"
region1 = "euw1"  # o "na1", "kr", etc.
try:
    total_hours = calculate_total_hours(summoner_name1, region1)
    print(f"El invocador {summoner_name1} ha jugado un total de {total_hours:.2f} horas en sus últimas partidas.")
except Exception as e:
    print(str(e))
