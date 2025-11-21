// Inserisci questo script nella cartella dove risiedono i tuoi HTML

function caricaTuttiCoworking(map, csvUrl) {
    Papa.parse(csvUrl, {
        download: true,
        header: true,
        complete: function(results) {
            const coworkingData = results.data;
            coworkingData.forEach(cw => {
                if (cw.lat && cw.lon) {
                    let popupContent = `
                        <b>${cw.name}</b><br>
                        ${cw.address ? cw.address + ',' : ''} ${cw.city}<br>
                        ${cw.website ? `<a href="${cw.website}" target="_blank">${cw.website}</a><br>` : ""}
                        ${cw.email ? `Email: <a href="mailto:${cw.email}">${cw.email}</a><br>` : ""}
                        ${cw.phone ? `Tel: ${cw.phone}<br>` : ""}
                        ${cw.services ? `Servizi: ${cw.services}<br>` : ""}
                        ${cw.opening_hours ? `Orari: ${cw.opening_hours}<br>` : ""}
                        ${cw.operator ? `Gestore: ${cw.operator}<br>` : ""}
                    `;
                    L.marker([parseFloat(cw.lat), parseFloat(cw.lon)])
                        .addTo(map)
                        .bindPopup(popupContent);
                }
            });
            map.setView([42.5, 12.5], 6); // Centro Italia
        }
    });
}