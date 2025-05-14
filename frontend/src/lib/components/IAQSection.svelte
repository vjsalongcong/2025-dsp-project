<script>
    import io from 'socket.io-client';
	import { onMount } from 'svelte';
    import { timestampValue, iaqStatus } from '$lib/logic/stores.js';
    import { flaskHost, flaskPort, flaskREST, flaskWebSocket } from '$lib/logic/host';
    
    // Import components
	import InfoCard from '$lib/components/InfoCard.svelte';

    // Import icons
    import droplet from '$lib/icons/droplet-fill.svg';
    import thermometer from '$lib/icons/thermometer.svg';

	// Initialise variables
	let co2Value = $state('...');
	let temperatureValue = $state('...');
	let humidityValue = $state('...');

	// Fetch data from REST endpoint
	async function fetchSensorValue() {
		try {
			const response = await fetch(`http://${flaskHost}:${flaskPort}/${flaskREST}`);
			if (response.ok) {
				const msg = await response.json();
				co2Value = `${msg.co2}`;
				temperatureValue = `${msg.temperature.toFixed(1)}`;
				humidityValue = `${msg.humidity.toFixed(1)}`;
                iaqStatus.set(msg.iaq_health);
                timestampValue.set(msg.timestamp);
			} else {
				console.error('Failed to fetch initial data');
			}
		} catch (error) {
			console.error('Error:', error);
		}
	}

    // Estalish WebSocket connection
	onMount(() => {
		// Initialise initial values from REST
		fetchSensorValue();

		// Connect to the Flask server
		const socket = io(`http://${flaskHost}:${flaskPort}`);

		// Listen for sensor data updates from the server
		socket.on(flaskWebSocket, (msg) => {
			co2Value = `${msg.co2}`;
			temperatureValue = `${msg.temperature.toFixed(1)}`;
			humidityValue = `${msg.humidity.toFixed(1)}`;
            iaqStatus.set(msg.iaq_health);
            timestampValue.set(msg.timestamp);
		});

		return () => {
			// Clean up when component is destroyed
			socket.disconnect();
		};
	});
</script>

<div class="grid grid-cols-1 gap-4">
    <div class="flex gap-4">

        <!-- Temperature Card -->
        <InfoCard
            title="Temperature"
            icon={thermometer}
            alt="Temperature-icon"
            value={temperatureValue}
            unit="°C"
        />

        <!-- Humidity Card -->
        <InfoCard
            title="Humidity"
            icon={droplet}
            alt="Humidity-icon"
            value={humidityValue}
            unit="%"
        />
        
    </div>

    <!-- Carbon Dioxide Card -->
    <InfoCard
        title="Carbon Dioxide"
        icon=""
        alt="CO₂"
        value={co2Value}
        unit="PPM"
    />

    <!-- Carbon Monoxide Card -->
    <InfoCard
        title="Carbon Monoxide"
        icon=""
        alt="CO"
        value="N/A"
        unit="PPM"
    />

    <!-- Nitrogen Dioxide Card -->
    <InfoCard
        title="Nitrogen Dioxide"
        icon=""
        alt="NO₂"
        value="N/A"
        unit="PPM"
    />

    <!-- Ammonia Card -->
    <InfoCard
        title="Ammonia"
        icon=""
        alt="NH₃"
        value="N/A"
        unit="PPM"
    />
</div>