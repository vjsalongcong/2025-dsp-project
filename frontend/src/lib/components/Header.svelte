<script lang="ts">
	import { page } from '$app/stores';

    // Import icons
	import settings from '$lib/icons/gear-fill.svg';
	import home from '$lib/icons/house-fill.svg';

    // Define navigation route icons
	const back = {
        // Go to Settings page
		'/': { title: "Dashboard", icon: settings, link: `/settings` },

        // Go to Home page
		'/settings': { title: "Settings", icon: home, link: `/` }
	};

    // Reactive statement to update the current route dynamically
    let currentRoute = $derived(() => back[$page.url.pathname as keyof typeof back]);
</script>

<header>
	<nav class="pb-5 flex">
		{#if currentRoute()}
			<!-- Render Page title -->
			<div class="flex-1">
				<h1 class="text-xl">{currentRoute().title}</h1>
			</div>

			<!-- Render the dynamic link and icon -->
			<div class="flex-none flex items-center">
					<a href={currentRoute().link}>
						<img src={currentRoute().icon} alt="Icon" />
					</a>
			</div>
		{:else}
			<p>An error has occurred, please return to the previous page</p>
		{/if}
	</nav>
</header>
