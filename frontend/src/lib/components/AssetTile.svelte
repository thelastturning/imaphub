<script>
    import ValidationBadge from "$lib/components/ValidationBadge.svelte";

    let {
        text = "",
        state = "neutral",
        type = "headline", // headline | description
        onStateChange,
        onEdit,
    } = $props();

    function cycleState() {
        const states = ["neutral", "selected", "rejected"];
        const currentIndex = states.indexOf(state);
        const nextIndex = (currentIndex + 1) % states.length;
        onStateChange(states[nextIndex]);
    }

    let stateClasses = $derived({
        neutral:
            "bg-white/[0.03] border-white/10 hover:border-white/20 hover:bg-white/[0.05]",
        selected:
            "bg-imap-primary/10 border-imap-primary/50 hover:border-imap-primary shadow-lg shadow-imap-primary/5",
        rejected:
            "bg-red-500/5 border-red-500/30 hover:border-red-500 hover:bg-red-500/10",
    });

    let textClasses = $derived({
        neutral: "text-gray-300",
        selected: "text-white font-medium",
        rejected: "text-red-300/60 line-through opacity-50",
    });

    // Character limit based on type
    let limit = $derived(type === "headline" ? 30 : 90);
</script>

<div
    class="relative p-5 border transition-all duration-300 cursor-pointer group {stateClasses[
        state
    ]} backdrop-blur-sm"
    onclick={cycleState}
    onkeydown={(e) => e.key === "Enter" && cycleState()}
    role="button"
    tabindex="0"
>
    <!-- State Overlay Glow -->
    {#if state === "selected"}
        <div
            class="absolute inset-0 bg-imap-primary/5 transition-opacity pointer-events-none"
        ></div>
    {/if}

    <!-- Edit Button -->
    <button
        class="absolute top-3 right-3 p-2 bg-black/60 hover:bg-imap-primary border border-white/10 opacity-0 group-hover:opacity-100 transition-all hover:scale-110 active:scale-90 z-20"
        onclick={(e) => {
            e.stopPropagation();
            onEdit();
        }}
        title="Bearbeiten"
    >
        <svg
            class="w-3.5 h-3.5 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
        >
            <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
            />
        </svg>
    </button>

    <!-- Text Content -->
    <p
        class="text-sm leading-relaxed {textClasses[
            state
        ]} pr-10 mb-5 select-none transition-colors duration-300"
    >
        {text}
    </p>

    <!-- Footer: Validation & State Indicators -->
    <div class="flex justify-between items-center relative z-10">
        <ValidationBadge {text} {limit} />

        <div class="flex items-center gap-2">
            {#if state === "selected"}
                <span
                    class="text-[10px] font-black text-imap-primary uppercase tracking-widest bg-imap-primary/10 px-2 py-0.5 rounded-full border border-imap-primary/20"
                    >Aktiv</span
                >
                <div
                    class="w-1.5 h-1.5 rounded-full bg-imap-primary shadow-[0_0_8px_#00A89E]"
                ></div>
            {:else if state === "rejected"}
                <span
                    class="text-[10px] font-black text-red-400 uppercase tracking-widest bg-red-400/10 px-2 py-0.5 rounded-full border border-red-400/20"
                    >Inaktiv</span
                >
                <div class="w-1.5 h-1.5 rounded-full bg-red-400"></div>
            {:else}
                <span
                    class="text-[8px] text-gray-600 uppercase font-black opacity-0 group-hover:opacity-100 transition-opacity"
                    >Status ändern</span
                >
                <div
                    class="w-1.5 h-1.5 rounded-full bg-gray-700 group-hover:bg-gray-500"
                ></div>
            {/if}
        </div>
    </div>
</div>

<style>
    /* Subtle inner shadow for selection */
    .border-imap-primary\/50 {
        box-shadow: inset 0 0 15px rgba(0, 168, 158, 0.05);
    }
</style>
