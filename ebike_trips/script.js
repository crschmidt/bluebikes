// script.js
let currentTripIndex = 0;
let tripsData = [];
let stationsData = {};
let map;
let markers = [];

function convertUtcToEastern(timeStr) {
    // Parse the UTC time using moment-timezone
    let easternTime = moment.tz(timeStr, "UTC").tz("America/New_York");

    // Format the date as needed
    return easternTime.format("YYYY-MM-DD HH:mm");
}

// Initialize the map
function initMap() {
    map = L.map('map-container'); 
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
}

// Load the JSON data
async function loadData() {
    let tripsResponse = await fetch('trips.json');
    let stationsResponse = await fetch('https://gbfs.lyft.com/gbfs/1.1/bos/en/station_information.json');
    tripsData = await tripsResponse.json();
    let stations = await stationsResponse.json();
    stations = stations.data.stations;

    // Convert stations array to a map for easy access
    stations.forEach(station => {
        stationsData[station.legacy_id] = station;
    });

}

// Display a specific trip
function displayTrip(index) {
    let trip = tripsData[index];
    let startStation = stationsData[trip.start];
    let endStation = stationsData[trip.end];

    // Clear existing markers
    markers.forEach(marker => marker.remove());
    markers = [];

    // Add markers to the map for start and end stations
    if (startStation && endStation) {
        markers.push(L.marker([startStation.lat, startStation.lon]).addTo(map).bindPopup('Start Station'));
        markers.push(L.marker([endStation.lat, endStation.lon]).addTo(map).bindPopup('End Station'));

        // Adjust map view
        map.fitBounds([
            [startStation.lat, startStation.lon],
            [endStation.lat, endStation.lon]
        ]);
    }

    // Display trip data in the sidebar
    let tripInfoElement = document.getElementById('trip-info');
    tripInfoElement.innerHTML = `
        <li>Start Time: ${convertUtcToEastern(trip.start_time)}</li>
        <li>End Time: ${convertUtcToEastern(trip.end_time)}</li>
	<li>Minutes: ${trip.min}</li>
        <li>Start Battery: ${trip.start_batt}%</li>
        <li>End Battery: ${trip.end_batt}%</li>
    `;
    updateUrlWithTripIndex(index);
}

// Function to get query parameters
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Function to update the URL with the current trip index
function updateUrlWithTripIndex(index) {
    if (history.pushState) {
        const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?trip=' + index;
        window.history.pushState({ path: newUrl }, '', newUrl);
    }
}


// Handle previous and next buttons
document.getElementById('prev-trip').addEventListener('click', () => {
    if (currentTripIndex > 0) {
        displayTrip(--currentTripIndex);
    }
});

document.getElementById('next-trip').addEventListener('click', () => {
    if (currentTripIndex < tripsData.length - 1) {
        displayTrip(++currentTripIndex);
    }
});

// Initialize
initMap();
loadData().then(() => {
    currentTripIndex = 0;	
    const tripIndexFromUrl = parseInt(getQueryParam('trip'));
    if (!isNaN(tripIndexFromUrl) && tripIndexFromUrl >= 0 && tripIndexFromUrl < tripsData.length) {
        currentTripIndex = tripIndexFromUrl;
    }
    displayTrip(currentTripIndex);
    updateUrlWithTripIndex(currentTripIndex); // Update URL when first loading the page
});
