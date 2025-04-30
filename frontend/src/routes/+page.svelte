<script>
	// Import components
	import IAQSection from '$lib/components/IAQSection.svelte';
	import SpriteCard from '$lib/components/SpriteCard.svelte'
</script>

<svelte:head>
	<title>Home</title>
	<meta name="View" content="View sensor data" />
</svelte:head>

<main>
	<div class="grid grid-cols-1 lg:grid-cols-2 min-h-screen gap-4">
		<!-- Main Content -->
		<div class="order-2 lg:order-1">
			<IAQSection />
		</div>
	  
		<!-- Sidebar / Right-aligned Element -->
		<div class="order-1 lg:order-2">
			<SpriteCard />
		</div>
	</div>
</main>
