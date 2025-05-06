async function getCoordenates(address){
    try {
        const req = await fetch(`https://nominatim.openstreetmap.org/search?q=${address}&format=json`);
        console.log(req)
        const response = await req.json();

        console.log(response);
        const coords = [response[0].lat, response[0].lon];
        console.log(coords);
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


            getCoordenates("ituiutaba").then((coords) => {
                let marker = L.circleMarker([coords[0], coords[1]], {
                    color: 'darkgreen',
                    radius: 1,
                    stroke: true,
                    weight: 0.8,
                    opacity: 1
                }).addTo(map);
            });
            
        }
);