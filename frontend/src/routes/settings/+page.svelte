<script>
	import { get } from 'svelte/store';
	import { onMount } from 'svelte';
	import { flaskHost, flaskPort, flaskAPI } from '$lib/logic/host';
	import { calibrationValues, thresholdValues, mqttValues } from '$lib/logic/stores';

	// Import components
	import IAQSection from '$lib/components/IAQSection.svelte';
	import SettingsCard from '$lib/components/SettingsCard.svelte';
	import SettingsInputForm from '$lib/components/SettingsInputForm.svelte';
	import CommitButton from '$lib/components/CommitButton.svelte';

	// Backend query urls
	let calibrationPath = `http://${flaskHost}:${flaskPort}/${flaskAPI}/iaq-calibration`
	let thresholdsPath = `http://${flaskHost}:${flaskPort}/${flaskAPI}/iaq-threshold`
	let mqttPath = `http://${flaskHost}:${flaskPort}/${flaskAPI}/mqtt`

	// Update calibration
	async function updateCalibration() {
		const calib = get(calibrationValues);

    	const res = await fetch(calibrationPath, {
    	  	method: 'POST',
    	  	headers: {
    	  	  	'Content-Type': 'application/json'
    	  	},
    	  	body: JSON.stringify(calib)
		});
    };

	// Update threshold
	async function updateThreshold() {
		const thresh = get(thresholdValues);

    	const res = await fetch(thresholdsPath, {
    	  	method: 'POST',
    	  	headers: {
    	  	  	'Content-Type': 'application/json'
    	  	},
    	  	body: JSON.stringify(thresh)
		});
    };

	// Update mqtt
	async function updateMQTT() {
		const mqtt = get(mqttValues);

    	const res = await fetch(mqttPath, {
    	  	method: 'POST',
    	  	headers: {
    	  	  	'Content-Type': 'application/json'
    	  	},
    	  	body: JSON.stringify(mqtt)
		});
    };

	// On page load
	onMount(async () => {
		try {
			// Initialise fetch
			const [calibRes, threshRes, mqttRes] = await Promise.all([
				fetch(calibrationPath),
				fetch(thresholdsPath),
				fetch(mqttPath)
			]);

			// If response error, log in console
			if (!calibRes.ok || !threshRes.ok || !mqttRes.ok) {
				console.log("Failed to fetch settings");
			}

			// Save response into variables
			calibrationValues.set(await calibRes.json());
			thresholdValues.set(await threshRes.json());
			mqttValues.set(await mqttRes.json());
		} catch (err) {
			console.log("Something else went wrong", err)
		}
	});
</script>

<svelte:head>
	<title>Settings</title>
	<meta name="Settings" content="Configure sensor data" />
</svelte:head>

<main>
	<div class="grid grid-cols-1 lg:grid-cols-2 min-h-screen gap-4">
		<!-- Main Content -->
		<div class="order-2 lg:order-1">
			<div class="grid gap-4">

				<!-- Calibration Configuration -->
				<form on:submit|preventDefault={updateCalibration}>
					<SettingsCard title="IAQ Calibration" description="Adjust the parameters below to calibrate Air Quality sensors.">

						<!-- Temperature Input -->
						<SettingsInputForm
							title="Temperature"
							placeholder=""
							type="number"
							id="c-temperature"
							bind:value={$calibrationValues["temperature"]}
						/>

						<!-- Humidity Input -->
						<SettingsInputForm
							title="Humidity"
							placeholder=""
							type="number"
							id="c-humidity"
							bind:value={$calibrationValues["humidity"]}
						/>

						<!-- Carbon Dioxide Input -->
						<SettingsInputForm
							title="Carbon Dioxide"
							placeholder=""
							type="number"
							id="c-carbon-dioxide"
							bind:value={$calibrationValues["carbon_dioxide"]}
						/>

						<!-- Carbon Monoxide Input -->
						<SettingsInputForm
							title="Carbon Monoxide"
							placeholder=""
							type="number"
							id="c-carbon-monoxide"
							bind:value={$calibrationValues["carbon_monoxide"]}
						/>

						<!-- Nitrogen Dioxide Input -->
						<SettingsInputForm
							title="Nitrogen Dioxide"
							placeholder=""
							type="number"
							id="c-nitrogen-dioxide"
							bind:value={$calibrationValues["nitrogen_dioxide"]}
						/>

						<!-- Ammonia Input -->
						<SettingsInputForm
							title="Ammonia"
							placeholder=""
							type="number"
							id="c-ammonia"
							bind:value={$calibrationValues["ammonia"]}
						/>

						<!-- Update Button -->
						<CommitButton text="Update" />
					</SettingsCard>
				</form>

				<!-- Threshold Configuration -->
				<form on:submit|preventDefault={updateThreshold}>
					<SettingsCard title="IAQ Threshold" description="Adjust thresholds to warn you of negative Air Quality.">

						<!-- Temperature Input -->
						<SettingsInputForm
							title="Max Temperature"
							placeholder=""
							type="number"
							id="t-max-temperature"
							bind:value="{$thresholdValues['max-temperature']}"
						/>

						<SettingsInputForm
							title="Min Temperature"
							placeholder=""
							type="number"
							id="t-min-temperature"
							bind:value="{$thresholdValues['min-temperature']}"
						/>

						<!-- Humidity Input -->
						<SettingsInputForm
							title="Max Humidity"
							placeholder=""
							type="number"
							id="t-max-humidity"
							bind:value="{$thresholdValues['max-humidity']}"
						/>

						<SettingsInputForm
							title="Min Humidity"
							placeholder=""
							type="number"
							id="t-min-humidity"
							bind:value="{$thresholdValues['min-humidity']}"
						/>

						<!-- Carbon Dioxide Input -->
						<SettingsInputForm
							title="Carbon Dioxide"
							placeholder=""
							type="number"
							id="t-carbon-dioxide"
							bind:value="{$thresholdValues['carbon_dioxide']}"

						/>

						<!-- Carbon Monoxide Input -->
						<SettingsInputForm
							title="Carbon Monoxide"
							placeholder=""
							type="number"
							id="t-carbon-monoxide"
							bind:value="{$thresholdValues['carbon_monoxide']}"
						/>

						<!-- Nitrogen Dioxide Input -->
						<SettingsInputForm
							title="Nitrogen Dioxide"
							placeholder=""
							type="number"
							id="t-nitrogen-dioxide"
							bind:value="{$thresholdValues['nitrogen_dioxide']}"
						/>

						<!-- Ammonia Input -->
						<SettingsInputForm
							title="Ammonia"
							placeholder=""
							type="number"
							id="t-ammonia"
							bind:value="{$thresholdValues['ammonia']}"
						/>

						<!-- Update Button -->
						<CommitButton text="Update" />
					</SettingsCard>
				</form>

				<!-- MQTT Server Configuration -->
				<form on:submit|preventDefault={updateMQTT}>
					<SettingsCard title="MQTT Server" description="Setup MQTT Server details to publish Air Quality data to.">

						<!-- MQTT Server Input -->
						<SettingsInputForm
							title="Server"
							placeholder=""
							type="text"
							id="mqtt-server"
							bind:value="{$mqttValues['broker']}"
						/>

						<!-- MQTT Port Input -->
						<SettingsInputForm
							title="Port"
							placeholder=""
							type="text"
							id="mqtt-port"
							bind:value="{$mqttValues['port']}"
						/>

						<!-- MQTT Topic Input -->
						<SettingsInputForm
							title="Topic"
							placeholder=""
							type="text"
							id="mqtt-topic"
							bind:value="{$mqttValues['topic']}"
						/>

						<!-- MQTT Username Input -->
						<SettingsInputForm
							title="Username"
							placeholder=""
							type="text"
							id="mqtt-username"
							bind:value="{$mqttValues['username']}"
						/>

						<!-- MQTT Password Input -->
						<SettingsInputForm
							title="Password"
							placeholder=""
							type="password"
							id="mqtt-password"
							bind:value="{$mqttValues['password']}"
						/>

						<!-- Update Button -->
						<CommitButton text="Save" />
					</SettingsCard>
				</form>

			</div>
		</div>
	
		<!-- Sidebar / Right-aligned Element (hidden on mobile) -->
		<div class="order-1 lg:order-2 hidden lg:block">
			<IAQSection />
		</div>
	</div>
</main>
