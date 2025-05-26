async function fetchObras(){
    try {
        const response = await fetch('http://localhost:8000/api/obras');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching obras: ", error);
    }
}

async function getCoordenates(address){
    try {
        const req = await fetch(`https://nominatim.openstreetmap.org/search?q=${address}&format=json`);
        const response = await req.json();

        
        const coords = [response[0].lat, response[0].lon];
        return coords;
    } catch (error) {
        console.error("Error fetching coordinates: ", error);
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

            fetchObras().then((obras) => {
                obras.forEach((obra) => {
                    const endereco = obra.cidade + " " + obra.bairro + " " + obra.rua + " " + obra.numero;
                    
                    getCoordenates(endereco).then((coords) => {
                        let marker = L.marker([coords[0], coords[1]]).addTo(map);
                        // Adiciona popup com informações da obra
                        let popupContent = `
                            <div style="min-width:180px">
                                <strong>${obra.nome || 'Obra sem nome'}</strong><br>
                                <span style="color:#555;">
                                    ${obra.rua}, ${obra.numero}<br>
                                    ${obra.bairro} - ${obra.cidade}
                                </span>
                            </div>
                        `;
                        marker.bindPopup(popupContent);
                    });
                });
            });
            
        }
);