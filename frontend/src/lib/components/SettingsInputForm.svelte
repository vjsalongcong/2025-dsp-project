<script>
    export let title;
    export let placeholder;
    export let type;
    export let id;
</script>

<div class="pb-2">
    <label for="{id}" class="block text-sm/6 font-medium text-gray-900">{title}</label>
    <div class="mt-2">
        <div class="flex items-center rounded-md bg-white px-3 outline-1 -outline-offset-1 outline-gray-300 has-[input:focus-within]:outline-2 has-[input:focus-within]:-outline-offset-2 has-[input:focus-within]:outline-indigo-600">
            <input type="{type}" name="{id}" id="{id}" class="block min-w-0 grow py-1.5 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6" placeholder="{placeholder}">
        </div>
    </div>
</div>