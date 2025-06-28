import requests
import time

def buscar_coordenadas_por_endereco(rua, numero, bairro, cidade):
    """
    Busca coordenadas (latitude, longitude) usando a API Nominatim do OpenStreetMap
    """
    try:
        # Construir o endereço completo
        endereco_completo = f"{rua}, {numero}, {bairro}, {cidade}, Brasil"
        
        # URL da API Nominatim
        url = "https://nominatim.openstreetmap.org/search"
        
        params = {
            'q': endereco_completo,
            'format': 'json',
            'limit': 1,
            'countrycodes': 'br'  # Limitar ao Brasil
        }
        
        headers = {
            'User-Agent': 'UaiRoute/1.0 (https://uairoute.app)'  # Obrigatório para Nominatim
        }
        
        # Fazer requisição
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data and len(data) > 0:
                result = data[0]
                latitude = float(result['lat'])
                longitude = float(result['lon'])
                
                print(f"Coordenadas encontradas para '{endereco_completo}': {latitude}, {longitude}")
                return latitude, longitude
            else:
                print(f"Nenhuma coordenada encontrada para '{endereco_completo}'")
                return None, None
        else:
            print(f"Erro na API Nominatim: {response.status_code}")
            return None, None
            
    except Exception as e:
        print(f"Erro ao buscar coordenadas: {str(e)}")
        return None, None

def buscar_coordenadas_com_fallback(rua, numero, bairro, cidade):
    """
    Busca coordenadas com fallback para endereços mais genéricos
    """
    # Tentar com endereço completo primeiro
    lat, lon = buscar_coordenadas_por_endereco(rua, numero, bairro, cidade)
    
    if lat is not None and lon is not None:
        return lat, lon
    
    # Tentar sem o número
    time.sleep(1)  # Rate limiting
    lat, lon = buscar_coordenadas_por_endereco(rua, "", bairro, cidade)
    
    if lat is not None and lon is not None:
        return lat, lon
    
    # Tentar só com a cidade
    time.sleep(1)  # Rate limiting
    lat, lon = buscar_coordenadas_por_endereco("", "", "", cidade)
    
    return lat, lon
