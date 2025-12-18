<script>
    import { fade, fly } from "svelte/transition";
    import Header from "$lib/components/Header.svelte";
    import AssetTile from "$lib/components/AssetTile.svelte";
    import { wizardStore } from "./store.svelte.js";
    import { Asset, AdGroup } from "$lib/models.svelte.js";

    // --- State ---
    let reportText = $state("");
    let isImportModalOpen = $state(false);
    let isUploading = $state(false);
    /** @type {string | null} */
    let uploadError = $state(null);

    // Navigation State
    // 'general' or adGroup.id
    let activeSectionId = $state("general");

    // Derived Data for Views
    /** @type {AdGroup | null | undefined} */
    let activeAdGroup = $derived(
        activeSectionId === "general"
            ? null
            : wizardStore.adGroups.find((ag) => ag.id === activeSectionId),
    );

    /** @type {Asset[]} */
    let activeHeadlines = $derived(
        activeAdGroup ? activeAdGroup.headlines : [],
    );
    /** @type {Asset[]} */
    let activeDescriptions = $derived(
        activeAdGroup ? activeAdGroup.descriptions : [],
    );

    // UI Helpers
    let selectedHeadlinesCount = $derived(
        activeHeadlines.filter((h) => h.state === "selected").length,
    );
    let selectedDescriptionsCount = $derived(
        activeDescriptions.filter((d) => d.state === "selected").length,
    );

    // --- Actions ---

    async function handleImportReport() {
        if (!reportText.trim()) {
            uploadError = "Bitte Berichtstext einfügen.";
            return;
        }

        isUploading = true;
        uploadError = null;

        try {
            const response = await fetch(
                "http://localhost:8000/api/v1/campaigns/import-report",
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        report_text: reportText,
                        customer_id: "demo-cust-001",
                    }),
                },
            );

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.message || "Import fehlgeschlagen");
            }

            const structure = await response.json();
            wizardStore.loadFromStructure(structure);

            // Close modal and keep General open (or switch to first AdGroup if user prefers?)
            // Staying on General allows them to check budget/name updates.
            isImportModalOpen = false;
        } catch (e) {
            uploadError =
                e instanceof Error
                    ? e.message
                    : "Ein unbekannter Fehler ist aufgetreten.";
        } finally {
            isUploading = false;
        }
    }

    /** @param {string} id */
    function setActiveSection(id) {
        activeSectionId = id;
    }
</script>

<div
    class="h-screen flex flex-col bg-[#050B0D] overflow-hidden text-imap-text font-sans"
>
    <Header path={["Hub", "CampaignWizard", "Neue Kampagne"]} />

    <main class="flex-1 w-full h-full relative overflow-hidden flex">
        <!-- LEFT SIDEBAR (Navigation) -->
        <aside
            class="w-[280px] bg-black/20 border-r border-white/5 flex flex-col shrink-0 z-20 backdrop-blur-sm"
        >
            <div class="p-6 border-b border-white/5">
                <h2 class="text-white font-bold text-lg">
                    {wizardStore.campaignName || "Kampagne erstellen"}
                </h2>
                <span
                    class="text-xs text-imap-primary uppercase tracking-widest font-bold"
                    >SETUP</span
                >
            </div>

            <nav class="flex-1 overflow-y-auto py-4 space-y-1">
                <!-- General Section -->
                <button
                    class="w-full text-left px-6 py-3 text-sm font-medium border-l-2 transition-colors
                            {activeSectionId === 'general'
                        ? 'border-imap-primary text-white bg-white/5'
                        : 'border-transparent text-gray-400 hover:text-white hover:bg-white/[0.02]'}"
                    onclick={() => setActiveSection("general")}
                >
                    Allgemeine Einstellungen
                </button>

                <div class="px-6 pt-6 pb-2 flex justify-between items-end">
                    <span
                        class="text-[10px] text-gray-500 uppercase font-black tracking-widest"
                        >Anzeigengruppen</span
                    >
                    <span class="text-[10px] text-gray-600 uppercase font-mono"
                        >{wizardStore.adGroups.length}</span
                    >
                </div>

                <!-- Ad Groups List -->
                {#each wizardStore.adGroups as ag (ag.id)}
                    <button
                        class="w-full text-left px-6 py-3 text-sm font-medium border-l-2 transition-colors flex justify-between items-center group
                                {activeSectionId === ag.id
                            ? 'border-imap-primary text-white bg-white/5'
                            : 'border-transparent text-gray-400 hover:text-white hover:bg-white/[0.02]'}"
                        onclick={() => setActiveSection(ag.id)}
                    >
                        <span class="truncate pr-2">{ag.name}</span>
                        {#if activeSectionId === ag.id}
                            <span
                                class="w-1.5 h-1.5 rounded-full bg-imap-primary"
                            ></span>
                        {/if}
                    </button>
                {/each}
            </nav>

            <div class="p-6 border-t border-white/5">
                <button
                    class="w-full py-3 bg-gradient-to-r from-imap-primary/20 to-imap-primary/10 hover:from-imap-primary/30 hover:to-imap-primary/20 text-white text-xs font-bold uppercase tracking-widest border border-imap-primary/30 transition-all shadow-[0_0_15px_rgba(0,168,158,0.1)] hover:shadow-[0_0_20px_rgba(0,168,158,0.3)]"
                    onclick={() => (isImportModalOpen = true)}
                >
                    ✨ Import Research
                </button>
            </div>
        </aside>

        <!-- RIGHT MAIN CONTENT -->
        <section
            class="flex-1 bg-[#071113] relative overflow-hidden flex flex-col"
        >
            <!-- Background -->
            <div
                class="absolute inset-0 bg-[radial-gradient(circle_at_10%_20%,_rgba(0,168,158,0.05),_transparent_40%)] pointer-events-none"
            ></div>

            <!-- Header for Section -->
            <header
                class="p-8 border-b border-white/5 z-10 bg-[#071113]/80 backdrop-blur-md"
            >
                {#if activeSectionId === "general"}
                    <h1 class="text-3xl text-white font-bold tracking-tight">
                        Allgemeine Einstellungen
                    </h1>
                    <p class="text-gray-400 text-sm mt-1">
                        Konfigurieren Sie globale Parameter manuell oder nutzen
                        Sie den Research-Import.
                    </p>
                {:else if activeAdGroup}
                    <div class="flex justify-between items-start">
                        <div>
                            <h1 class="text-2xl text-white font-bold">
                                {activeAdGroup.name}
                            </h1>
                            <p class="text-gray-400 text-sm mt-1">
                                Verwalten Sie Assets für dieses Segment.
                            </p>
                        </div>
                        <div class="flex gap-2">
                            <span
                                class="px-3 py-1 bg-white/5 border border-white/10 rounded text-xs text-gray-300 font-mono"
                            >
                                {selectedHeadlinesCount} / 15 Anzeigentitel
                            </span>
                            <span
                                class="px-3 py-1 bg-white/5 border border-white/10 rounded text-xs text-gray-300 font-mono"
                            >
                                {selectedDescriptionsCount} / 4 Beschreibungen
                            </span>
                        </div>
                    </div>
                {/if}
            </header>

            <!-- Content Area -->
            <div class="flex-1 overflow-y-auto p-8 custom-scrollbar z-10">
                {#if activeSectionId === "general"}
                    <!-- GENERAL FORM -->
                    <div
                        class="max-w-4xl space-y-8"
                        in:fly={{ y: 10, duration: 300 }}
                    >
                        <!-- Row 1 -->
                        <div class="grid grid-cols-2 gap-6">
                            <div
                                class="bg-white/[0.02] border border-white/10 p-6"
                            >
                                <label
                                    class="block text-gray-400 text-[10px] font-bold uppercase tracking-widest mb-3"
                                    >Kampagnenname</label
                                >
                                <input
                                    type="text"
                                    bind:value={wizardStore.campaignName}
                                    placeholder="e.g. Q4 Performance Max"
                                    class="w-full bg-black/40 border border-white/10 p-3 text-white focus:border-imap-primary outline-none transition-colors"
                                />
                            </div>

                            <div
                                class="bg-white/[0.02] border border-white/10 p-6"
                            >
                                <label
                                    class="block text-gray-400 text-[10px] font-bold uppercase tracking-widest mb-3"
                                    >Budget (Täglich)</label
                                >
                                <div class="relative">
                                    <span
                                        class="absolute left-4 top-3 text-gray-500"
                                        >€</span
                                    >
                                    <input
                                        type="number"
                                        bind:value={wizardStore.budget}
                                        class="w-full bg-black/40 border border-white/10 p-3 pl-8 text-white focus:border-imap-primary outline-none transition-colors"
                                    />
                                </div>
                            </div>
                        </div>

                        <!-- Row 2 -->
                        <div class="grid grid-cols-2 gap-6">
                            <div
                                class="bg-white/[0.02] border border-white/10 p-6"
                            >
                                <label
                                    class="block text-gray-400 text-[10px] font-bold uppercase tracking-widest mb-3"
                                    >Language</label
                                >
                                <div class="relative">
                                    <select
                                        bind:value={wizardStore.language}
                                        class="w-full bg-black/40 border border-white/10 p-3 text-white focus:border-imap-primary outline-none appearance-none cursor-pointer"
                                    >
                                        <option value="de">Deutsch (DE)</option>
                                        <option value="en">English (EN)</option>
                                    </select>
                                    <span
                                        class="absolute right-4 top-3.5 text-gray-500 pointer-events-none text-xs"
                                        >▼</span
                                    >
                                </div>
                            </div>

                            <div
                                class="bg-white/[0.02] border border-white/10 p-6"
                            >
                                <label
                                    class="block text-gray-400 text-[10px] font-bold uppercase tracking-widest mb-3"
                                    >Targeting (DACH)</label
                                >
                                <div class="flex gap-2">
                                    {#each ["Germany", "Austria", "Switzerland"] as loc}
                                        <button
                                            class="flex-1 py-2 px-3 text-[10px] font-bold border transition-all
                                                   {wizardStore.targetLocations.includes(
                                                loc,
                                            )
                                                ? 'bg-imap-primary/20 border-imap-primary text-imap-primary shadow-[0_0_10px_rgba(0,168,158,0.2)]'
                                                : 'bg-black/40 border-white/10 text-gray-500 hover:border-white/30'}"
                                            onclick={() => {
                                                if (
                                                    wizardStore.targetLocations.includes(
                                                        loc,
                                                    )
                                                ) {
                                                    wizardStore.targetLocations =
                                                        wizardStore.targetLocations.filter(
                                                            (l) => l !== loc,
                                                        );
                                                } else {
                                                    wizardStore.targetLocations =
                                                        [
                                                            ...wizardStore.targetLocations,
                                                            loc,
                                                        ];
                                                }
                                            }}
                                        >
                                            {loc === "Germany"
                                                ? "DE"
                                                : loc === "Austria"
                                                  ? "AT"
                                                  : "CH"}
                                        </button>
                                    {/each}
                                </div>
                                <p
                                    class="text-[9px] text-gray-500 mt-2 uppercase tracking-tighter"
                                >
                                    Maps to Google Geo-Targeting database
                                </p>
                            </div>
                        </div>

                        <!-- Row 3 -->
                        <div class="bg-white/[0.02] border border-white/10 p-6">
                            <label
                                class="block text-gray-400 text-[10px] font-bold uppercase tracking-widest mb-3"
                                >Kampagnenziel</label
                            >
                            <div class="flex gap-4">
                                <button
                                    class="px-6 py-3 border text-sm font-bold transition-all {wizardStore.objective ===
                                    'LEADS'
                                        ? 'bg-imap-primary/20 border-imap-primary text-imap-primary shadow-[0_0_10px_rgba(0,168,158,0.2)]'
                                        : 'bg-black/40 border-white/10 text-gray-400 hover:border-white/30'}"
                                    onclick={() =>
                                        (wizardStore.objective = "LEADS")}
                                >
                                    LEADS
                                </button>
                                <button
                                    class="px-6 py-3 border text-sm font-bold transition-all {wizardStore.objective ===
                                    'SALES'
                                        ? 'bg-imap-primary/20 border-imap-primary text-imap-primary shadow-[0_0_10px_rgba(0,168,158,0.2)]'
                                        : 'bg-black/40 border-white/10 text-gray-400 hover:border-white/30'}"
                                    onclick={() =>
                                        (wizardStore.objective = "SALES")}
                                >
                                    UMSÄTZE
                                </button>
                                <button
                                    class="px-6 py-3 border text-sm font-bold transition-all {wizardStore.objective ===
                                    'TRAFFIC'
                                        ? 'bg-imap-primary/20 border-imap-primary text-imap-primary shadow-[0_0_10px_rgba(0,168,158,0.2)]'
                                        : 'bg-black/40 border-white/10 text-gray-400 hover:border-white/30'}"
                                    onclick={() =>
                                        (wizardStore.objective = "TRAFFIC")}
                                >
                                    ZUGRIFFE
                                </button>
                            </div>
                        </div>
                    </div>
                {:else if activeAdGroup}
                    <!-- AD GROUP ASSETS -->
                    {#key activeAdGroup.id}
                        <div
                            class="grid grid-cols-2 gap-8"
                            in:fly={{ y: 10, duration: 300 }}
                        >
                            <!-- Headlines -->
                            <div>
                                <div class="flex items-center gap-2 mb-4">
                                    <span class="w-1 h-4 bg-imap-primary"
                                    ></span>
                                    <h3 class="text-white font-bold">
                                        Anzeigentitel
                                    </h3>
                                </div>
                                <div class="space-y-3">
                                    {#each activeHeadlines as h (h.id)}
                                        <AssetTile
                                            text={h.text}
                                            state={h.state}
                                            type="headline"
                                            onStateChange={(
                                                /** @type {'neutral' | 'selected' | 'rejected'} */ s,
                                            ) => (h.state = s)}
                                            onEdit={() => {}}
                                        />
                                    {/each}
                                </div>
                            </div>

                            <!-- Descriptions -->
                            <div>
                                <div class="flex items-center gap-2 mb-4">
                                    <span class="w-1 h-4 bg-imap-primary"
                                    ></span>
                                    <h3 class="text-white font-bold">
                                        Beschreibungen
                                    </h3>
                                </div>
                                <div class="space-y-3">
                                    {#each activeDescriptions as d (d.id)}
                                        <AssetTile
                                            text={d.text}
                                            state={d.state}
                                            type="description"
                                            onStateChange={(
                                                /** @type {'neutral' | 'selected' | 'rejected'} */ s,
                                            ) => (d.state = s)}
                                            onEdit={() => {}}
                                        />
                                    {/each}
                                </div>
                            </div>
                        </div>
                    {/key}
                {/if}
            </div>
        </section>

        <!-- IMPORT MODAL -->
        {#if isImportModalOpen}
            <div
                class="absolute inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-8"
                transition:fade
            >
                <div
                    class="w-full max-w-3xl bg-[#0a1518] border border-white/10 shadow-2xl relative flex flex-col max-h-full"
                >
                    <!-- Modal Header -->
                    <div
                        class="p-6 border-b border-white/10 flex justify-between items-center bg-white/[0.02]"
                    >
                        <div>
                            <h3 class="text-xl text-white font-bold">
                                Deep Research Importieren
                            </h3>
                            <p class="text-gray-400 text-xs mt-1">
                                Fügen Sie Ihren Gemini-Research-Bericht ein, um
                                Inhalte automatisch zu generieren.
                            </p>
                        </div>
                        <button
                            class="w-8 h-8 flex items-center justify-center rounded-full bg-white/5 hover:bg-white/10 text-gray-400 transition-colors"
                            onclick={() => (isImportModalOpen = false)}
                        >
                            ✕
                        </button>
                    </div>

                    <!-- Modal Body -->
                    <div class="p-6 flex-1 overflow-hidden flex flex-col">
                        <textarea
                            bind:value={reportText}
                            placeholder="Berichtsinhalt hier einfügen..."
                            class="flex-1 bg-black/40 border border-white/10 p-5 text-gray-300 text-sm focus:border-imap-primary outline-none resize-none custom-scrollbar font-mono mb-6"
                        ></textarea>

                        <div class="flex justify-between items-center shrink-0">
                            {#if uploadError}
                                <span
                                    class="text-red-400 text-sm flex items-center gap-2"
                                    >⚠️ {uploadError}</span
                                >
                            {:else}
                                <span class="text-gray-500 text-xs italic"
                                    >Dies wird Anzeigengruppen und Assets
                                    füllen.</span
                                >
                            {/if}

                            <div class="flex flex-col items-end gap-2">
                                <button
                                    onclick={handleImportReport}
                                    disabled={isUploading}
                                    class="px-8 py-3 bg-imap-primary hover:bg-imap-primary-hover text-white font-bold transition-all flex items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {#if isUploading}
                                        <svg
                                            class="animate-spin h-4 w-4 text-white"
                                            xmlns="http://www.w3.org/2000/svg"
                                            fill="none"
                                            viewBox="0 0 24 24"
                                        >
                                            <circle
                                                class="opacity-25"
                                                cx="12"
                                                cy="12"
                                                r="10"
                                                stroke="currentColor"
                                                stroke-width="4"
                                            ></circle>
                                            <path
                                                class="opacity-75"
                                                fill="currentColor"
                                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                                            ></path>
                                        </svg>
                                        Analysiere...
                                    {:else}
                                        <span>🚀</span> Inhalte generieren
                                    {/if}
                                </button>
                                {#if isUploading}
                                    <span
                                        class="text-[10px] text-imap-primary animate-pulse"
                                        >KI arbeitet, dies kann bis zu 30s
                                        dauern...</span
                                    >
                                {/if}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        {/if}
    </main>
</div>

<style>
    .custom-scrollbar::-webkit-scrollbar {
        width: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.02);
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: rgba(0, 168, 158, 0.2);
    }
</style>
