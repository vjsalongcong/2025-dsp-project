<script>
	import { timestampValue, iaqStatus } from '$lib/logic/stores.js';

    // Import sprite
	import day_healthy from '$lib/sprite/bird_day_healthy.png';
	import day_dead from '$lib/sprite/bird_day_dead.png';
	import night_healthy from '$lib/sprite/bird_night_healthy.png';
	import night_dead from '$lib/sprite/bird_night_dead.png';

	// Determine if it's daytime based on the timestamp
	$: isDay = $timestampValue
    	? (new Date($timestampValue).getHours() >= 6 && new Date($timestampValue).getHours() < 18)
    	: true;

	// Determine if the bird is healthy or dead
	$: birdState = $iaqStatus === 'good' ? 'healthy' : 'dead';

	// Choose the correct image
	$: sprite = (() => {
    	if (isDay && birdState === 'healthy') return day_healthy;
    	if (isDay && birdState === 'dead') return day_dead;
    	if (!isDay && birdState === 'healthy') return night_healthy;
    	return night_dead;
  	})();
</script>

{#if $timestampValue !== null && $iaqStatus}
	<img class="rounded-lg bg-white shadow-lg" src="{sprite}" alt="Bird sprite" />
{:else}
	<img class="rounded-lg bg-white shadow-lg" src="{night_healthy}" alt="Bird sprite" />
{/if}