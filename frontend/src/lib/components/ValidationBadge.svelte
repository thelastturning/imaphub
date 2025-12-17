<script>
    let { text = "", limit = 30 } = $props();

    // Derived state for character count
    let count = $derived(text.length);
    let isOverLimit = $derived(count > limit);
    let isNearLimit = $derived(count > limit * 0.9 && !isOverLimit);
</script>

<div
    class="flex items-center gap-1 text-xs font-mono transition-colors duration-200"
    class:text-red-500={isOverLimit}
    class:text-yellow-500={isNearLimit}
    class:text-gray-400={!isOverLimit && !isNearLimit}
>
    <span>{count}</span>
    <span class="text-gray-600">/</span>
    <span>{limit}</span>

    {#if isOverLimit}
        <!-- Warning Icon -->
        <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-3 w-3 ml-1"
            viewBox="0 0 20 20"
            fill="currentColor"
        >
            <path
                fill-rule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                clip-rule="evenodd"
            />
        </svg>
    {/if}
</div>
