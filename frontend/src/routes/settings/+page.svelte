<script>
	// Import components
	import IAQSection from '$lib/components/IAQSection.svelte';
	import SettingsCard from '$lib/components/SettingsCard.svelte';
	import SettingsInputForm from '$lib/components/SettingsInputForm.svelte'
	import CommitButton from '$lib/components/CommitButton.svelte'
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
				<SettingsCard title="IAQ Calibration" description="Adjust the parameters below to calibrate Air Quality sensors.">

					<!-- Temperature Input -->
					<SettingsInputForm
						title="Temperature"
						placeholder="0"
						type="number"
						id="c-temperature"
					/>

					<!-- Humidity Input -->
					<SettingsInputForm
						title="Humidity"
						placeholder="0"
						type="number"
						id="c-humidity"
					/>

					<!-- Carbon Dioxide Input -->
					<SettingsInputForm
						title="Carbon Dioxide"
						placeholder="0"
						type="number"
						id="c-carbon-dioxide"
					/>

					<!-- Carbon Monoxide Input -->
					<SettingsInputForm
						title="Carbon Monoxide"
						placeholder="0"
						type="number"
						id="c-carbon-monoxide"
					/>

					<!-- Nitrogen Dioxide Input -->
					<SettingsInputForm
						title="Nitrogen Dioxide"
						placeholder="0"
						type="number"
						id="c-nitrogen-dioxide"
					/>

					<!-- Ammonia Input -->
					<SettingsInputForm
						title="Ammonia"
						placeholder="0"
						type="number"
						id="c-ammonia"
					/>

					<!-- Update Button -->
					<CommitButton text="Update" />
				</SettingsCard>

				<!-- Threshold Configuration -->
				<SettingsCard title="IAQ Threshold" description="Adjust thresholds to warn you of negative Air Quality.">

					<!-- Temperature Input -->
					<SettingsInputForm
						title="Max Temperature"
						placeholder="25"
						type="number"
						id="t-max-temperature"
					/>

					<SettingsInputForm
						title="Min Temperature"
						placeholder="15"
						type="number"
						id="t-min-temperature"
					/>

					<!-- Humidity Input -->
					<SettingsInputForm
						title="Max Humidity"
						placeholder="65"
						type="number"
						id="t-max-humidity"
					/>

					<SettingsInputForm
						title="Min Humidity"
						placeholder="25"
						type="number"
						id="t-max-humidity"
					/>

					<SettingsInputForm
						title="Humidity"
						placeholder="65"
						type="number"
						id="t-humidity"
					/>

					<!-- Carbon Dioxide Input -->
					<SettingsInputForm
						title="Carbon Dioxide"
						placeholder="1000"
						type="number"
						id="t-carbon-dioxide"
					/>

					<!-- Carbon Monoxide Input -->
					<SettingsInputForm
						title="Carbon Monoxide"
						placeholder="0"
						type="number"
						id="c-carbon-monoxide"
					/>

					<!-- Nitrogen Dioxide Input -->
					<SettingsInputForm
						title="Nitrogen Dioxide"
						placeholder="0"
						type="number"
						id="t-nitrogen-dioxide"
					/>

					<!-- Ammonia Input -->
					<SettingsInputForm
						title="Ammonia"
						placeholder="0"
						type="number"
						id="t-ammonia"
					/>

					<!-- Update Button -->
					<CommitButton text="Update" />
				</SettingsCard>

				<!-- MQTT Server Configuration -->
				<SettingsCard title="MQTT Server" description="Setup MQTT Server details to publish Air Quality data to.">

					<!-- MQTT Server Input -->
					<SettingsInputForm
						title="Server"
						placeholder="127.0.0.1"
						type="text"
						id="mqtt-server"
					/>

					<!-- MQTT Port Input -->
					<SettingsInputForm
						title="Port"
						placeholder="1883"
						type="text"
						id="mqtt-port"
					/>

					<!-- MQTT Topic Input -->
					<SettingsInputForm
						title="Topic"
						placeholder="raspberrypi/mqtt"
						type="text"
						id="mqtt-topic"
					/>

					<!-- MQTT Username Input -->
					<SettingsInputForm
						title="Username"
						placeholder="Enter the username"
						type="text"
						id="mqtt-username"
					/>

					<!-- MQTT Password Input -->
					<SettingsInputForm
						title="Password"
						placeholder="Enter the password"
						type="text"
						id="mqtt-password"
					/>

					<!-- Update Button -->
					<CommitButton text="Save" />
				</SettingsCard>
			</div>
		</div>
	
		<!-- Sidebar / Right-aligned Element (hidden on mobile) -->
		<div class="order-1 lg:order-2 hidden lg:block">
			<IAQSection />
		</div>
	</div>
</main>
