<script>
    export let title;
    export let icon;
    export let alt;
    export let value;
    export let unit = "";
</script>

<div class="p-4 flex-1 rounded-lg items-center justify-center bg-white shadow-lg">
    <!-- Top section -->
    <div class="flex">
        <div class="flex-1 text-start">{title}</div>
        <div class="flex-1 flex justify-end">
            <img src={icon} alt={`${alt}`} />
        </div>
    </div>

    <!-- Value section -->
    <div class="pt-3 text-5xl text-start">
        {value}
        {#if unit}
            <div class="text-xl inline-block text-gray-500">{unit}</div>
        {/if}
    </div>
</div>
