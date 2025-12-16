<script lang="ts">
    export let text: string;
    export let state: 'neutral' | 'selected' | 'rejected' = 'neutral';
    export let onStateChange: (newState: 'neutral' | 'selected' | 'rejected') => void;
    export let onEdit: () => void;

    function cycleState() {
        const states: Array<'neutral' | 'selected' | 'rejected'> = ['neutral', 'selected', 'rejected'];
        const currentIndex = states.indexOf(state);
        const nextIndex = (currentIndex + 1) % states.length;
        onStateChange(states[nextIndex]);
    }

    $: stateClasses = {
        neutral: 'bg-gray-700/50 border-white/10 hover:border-white/20',
        selected: 'bg-teal-900/20 border-imap-primary/50 hover:border-imap-primary',
        rejected: 'bg-red-900/20 border-red-500/50 hover:border-red-500'
    };

    $: textClasses = {
        neutral: 'text-gray-300',
        selected: 'text-teal-100',
        rejected: 'text-red-100'
    };
</script>

<div
    class="relative p-4 border transition-all cursor-pointer group {stateClasses[state]}"
    on:click={cycleState}
    on:keydown={(e) => e.key === 'Enter' && cycleState()}
    role="button"
    tabindex="0"
>
    <!-- Edit Button -->
    <button
        class="absolute top-2 right-2 p-1.5 bg-black/40 hover:bg-black/60 border border-white/10 opacity-0 group-hover:opacity-100 transition-opacity"
        on:click|stopPropagation={onEdit}
        title="Edit"
    >
        <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
        </svg>
    </button>

    <!-- Text Content -->
    <p class="text-sm leading-relaxed {textClasses[state]} pr-8">
        {text}
    </p>

    <!-- State Indicator -->
    <div class="absolute bottom-2 right-2 flex gap-1">
        <div class="w-2 h-2 {state === 'neutral' ? 'bg-gray-500' : 'bg-transparent'}"></div>
        <div class="w-2 h-2 {state === 'selected' ? 'bg-imap-primary' : 'bg-transparent'}"></div>
        <div class="w-2 h-2 {state === 'rejected' ? 'bg-red-500' : 'bg-transparent'}"></div>
    </div>
</div>
