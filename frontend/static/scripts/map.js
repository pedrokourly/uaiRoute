async function fetchObras(){
    try {
        const response = await fetch('http://localhost:8000/api/obras');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching obras: ", error);
        return [];
    }
}

async function fetchVeiculos(){
    try {
        const response = await fetch('http://localhost:8000/api/veiculos');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching veiculos: ", error);
        return [];
    }
}

async function fetchAlojamentos(){
    try {
        const response = await fetch('http://localhost:8000/api/alojamento');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching alojamentos: ", error);
        return [];
    }
}

async function getCoordenates(address){
    try {
        const req = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(address)}&format=json&limit=1`);
        const response = await req.json();

        if (response && response.length > 0) {
            const coords = [parseFloat(response[0].lat), parseFloat(response[0].lon)];
            return coords;
        }
        return null;
    } catch (error) {
        console.error("Error fetching coordinates: ", error);
        return null;
    }
}

$(document).ready(function () {
            // Mapa
            var map = L.map('map', {
                fullscreenControl: true,
                fullscreenControlOptions: { position: 'topleft' }
            });

            // Visualização
            map.setView([-18.918999, -48.277950], 7);

            // Atribuição
            var attb = '&copy; <a target="_blank" href="https://www.maptiler.com/copyright/">MapTiler</a>, &copy; <a target = "_blank" href="https://www.openstreetmap.org/">OpenStreetMap</a>, <a href="https://github.com/pedrokourly/uaiRoute" target="_blank">uaiRoute</a>';

            // Chave API MapTiler
            const key = 'jlq6npehL8CYWBPs1v4S';
            
            // Camada Base
            L.tileLayer(`https://api.maptiler.com/maps/streets-v2/{z}/{x}/{y}.png?key=${key}`,{ //style URL
                attribution: attb,
                tileSize: 512,
                zoomOffset: -1,
                crossOrigin: true
            }).addTo(map);

            // Barra de Pesquisa
            L.control.maptilerGeocoding({ 
                apiKey: key 
            }).addTo(map);
            
            // Resetar Visualização
            L.control.resetView({
                position: "topleft",
                title: "Reset view",
                latlng: L.latLng([-18.918999, -48.277950]),
                zoom: 7
            }).addTo(map);

            // Definir ícones personalizados para diferentes entidades
            const obrasIcon = L.divIcon({
                className: 'custom-marker obras-marker',
                html: '<div style="background-color: #dc3545; color: white; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">🏗️</div>',
                iconSize: [25, 25],
                iconAnchor: [12, 12]
            });

            const veiculosIcon = L.divIcon({
                className: 'custom-marker veiculos-marker',
                html: '<div style="background-color: #28a745; color: white; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">🚗</div>',
                iconSize: [25, 25],
                iconAnchor: [12, 12]
            });

            const alojamentosIcon = L.divIcon({
                className: 'custom-marker alojamentos-marker',
                html: '<div style="background-color: #007bff; color: white; border-radius: 50%; width: 25px; height: 25px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">🏠</div>',
                iconSize: [25, 25],
                iconAnchor: [12, 12]
            });

            // Carregar e exibir todas as entidades no mapa
            Promise.all([fetchObras(), fetchVeiculos(), fetchAlojamentos()]).then(([obras, veiculos, alojamentos]) => {
                let totalEntidades = obras.length + veiculos.length + alojamentos.length;
                
                // Atualizar contador no HTML
                $('#obras-count-num').text(totalEntidades);
                $('#obras-count').fadeIn();
                
                // Adicionar obras (vermelho)
                obras.forEach((obra) => {
                    const endereco = obra.cidade + " " + obra.bairro + " " + obra.rua + " " + obra.numero;
                    
                    getCoordenates(endereco).then((coords) => {
                        if (coords) {
                            let marker = L.marker([coords[0], coords[1]], {icon: obrasIcon}).addTo(map);
                            let popupContent = `
                                <div style="min-width:200px">
                                    <div style="background: #dc3545; color: white; padding: 8px; margin: -10px -10px 10px -10px; border-radius: 4px 4px 0 0;">
                                        <strong>🏗️ OBRA</strong>
                                    </div>
                                    <strong>${obra.nome || 'Obra sem nome'}</strong><br>
                                    <span style="color:#555;">
                                        ${obra.rua}, ${obra.numero}<br>
                                        ${obra.bairro} - ${obra.cidade}
                                    </span>
                                </div>
                            `;
                            marker.bindPopup(popupContent);
                        }
                    });
                });

                // Adicionar veículos (verde)
                veiculos.forEach((veiculo) => {
                    // Para veículos, vamos usar um endereço genérico ou última localização conhecida
                    // Como não temos campo de localização específico, vamos usar a cidade como referência
                    const endereco = "Ituiutaba, MG"; // Endereço padrão ou você pode usar outro campo se disponível
                    
                    getCoordenates(endereco).then((coords) => {
                        if (coords) {
                            // Adicionar um pequeno offset aleatório para evitar sobreposição
                            const lat = parseFloat(coords[0]) + (Math.random() - 0.5) * 0.01;
                            const lng = parseFloat(coords[1]) + (Math.random() - 0.5) * 0.01;
                            
                            let marker = L.marker([lat, lng], {icon: veiculosIcon}).addTo(map);
                            let popupContent = `
                                <div style="min-width:200px">
                                    <div style="background: #28a745; color: white; padding: 8px; margin: -10px -10px 10px -10px; border-radius: 4px 4px 0 0;">
                                        <strong>🚗 VEÍCULO</strong>
                                    </div>
                                    <strong>${veiculo.modelo || 'Modelo não informado'}</strong><br>
                                    <span style="color:#555;">
                                        Placa: ${veiculo.placa || 'N/A'}<br>
                                        Marca: ${veiculo.marca || 'N/A'}
                                    </span>
                                </div>
                            `;
                            marker.bindPopup(popupContent);
                        }
                    });
                });

                // Adicionar alojamentos (azul)
                alojamentos.forEach((alojamento) => {
                    const endereco = alojamento.cidade + " " + alojamento.bairro + " " + alojamento.rua + " " + alojamento.numero;
                    
                    getCoordenates(endereco).then((coords) => {
                        if (coords) {
                            let marker = L.marker([coords[0], coords[1]], {icon: alojamentosIcon}).addTo(map);
                            let popupContent = `
                                <div style="min-width:200px">
                                    <div style="background: #007bff; color: white; padding: 8px; margin: -10px -10px 10px -10px; border-radius: 4px 4px 0 0;">
                                        <strong>🏠 ALOJAMENTO</strong>
                                    </div>
                                    <strong>${alojamento.nome || 'Alojamento sem nome'}</strong><br>
                                    <span style="color:#555;">
                                        ${alojamento.rua}, ${alojamento.numero}<br>
                                        ${alojamento.bairro} - ${alojamento.cidade}<br>
                                        Capacidade: ${alojamento.capacidade_maxima} pessoas<br>
                                        Vagas disponíveis: ${alojamento.vagas_disponiveis || alojamento.capacidade_maxima}
                                    </span>
                                </div>
                            `;
                            marker.bindPopup(popupContent);
                        }
                    });
                });
            });
            
        }
);