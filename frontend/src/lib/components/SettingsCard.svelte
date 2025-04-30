<script>
    export let title;
    export let description;
</script>

<div class="p-4 flex-1 rounded-lg items-center justify-center bg-white shadow-lg">
    <!-- Title -->
    <div class="flex-1 text-start text-xl font-semibold pb-1">{title}</div>

    <!-- Description -->
    <p class="text-xs text-gray-900 pb-3">{description}</p>
    <slot />
</div>
