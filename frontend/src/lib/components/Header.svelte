<script lang="ts">
    // Header Component
    let logoError = $state(false);
</script>

<header
    class="h-16 w-full bg-imap-header shadow-lg shadow-black/20 border-b border-white/10 flex items-center justify-between px-6 shrink-0 z-50 relative"
>
    <!-- Left: Logo & Title -->
    <div class="flex items-center gap-3">
        <!-- Logo Placeholder -->
        <div class="h-8 w-8 flex items-center justify-center">
            {#if !logoError}
                <img
                    src="/src/lib/assets/images/logo.svg"
                    alt="IMAP Logo"
                    class="h-full w-full object-contain"
                    onerror={() => (logoError = true)}
                />
            {:else}
                <span
                    class="text-white font-bold text-xs border border-white p-1"
                    >LOGO</span
                >
            {/if}
        </div>

        <span class="text-white font-semibold text-lg tracking-wide">
            IMAP CampaignWizard
        </span>
    </div>

    <!-- Right: User Avatar -->
    <div class="flex items-center gap-4">
        <div
            class="w-9 h-9 bg-imap-primary rounded-full flex items-center justify-center text-white font-bold shadow-md cursor-pointer hover:bg-imap-primary-hover transition-colors"
        >
            U
        </div>
    </div>
</header>
