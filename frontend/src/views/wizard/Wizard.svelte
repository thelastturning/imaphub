<script lang="ts">
    import Header from "$lib/components/Header.svelte";
    import AssetTile from "$lib/components/AssetTile.svelte";

    type AssetState = "neutral" | "selected" | "rejected";

    interface Asset {
        id: number;
        text: string;
        state: AssetState;
    }

    // Dummy Data
    let headlines: Asset[] = [
        {
            id: 1,
            text: "Revolutionize Your Marketing Strategy",
            state: "neutral",
        },
        {
            id: 2,
            text: "Boost ROI with AI-Powered Campaigns",
            state: "neutral",
        },
        { id: 3, text: "Transform Your Business Today", state: "neutral" },
        {
            id: 4,
            text: "Unlock Growth with Smart Automation",
            state: "neutral",
        },
        {
            id: 5,
            text: "Experience the Future of Advertising",
            state: "neutral",
        },
        {
            id: 6,
            text: "Drive Results with Data-Driven Insights",
            state: "neutral",
        },
    ];

    let descriptions: Asset[] = [
        {
            id: 7,
            text: "Discover cutting-edge tools designed to elevate your campaigns and maximize your advertising budget.",
            state: "neutral",
        },
        {
            id: 8,
            text: "Join thousands of businesses achieving unprecedented growth with our proven platform.",
            state: "neutral",
        },
        {
            id: 9,
            text: "Streamline your workflow and focus on what matters most - growing your business.",
            state: "neutral",
        },
        {
            id: 10,
            text: "Get started in minutes with our intuitive interface and expert support team.",
            state: "neutral",
        },
    ];

    function updateHeadlineState(id: number, newState: AssetState) {
        headlines = headlines.map((h) =>
            h.id === id ? { ...h, state: newState } : h,
        );
    }

    function updateDescriptionState(id: number, newState: AssetState) {
        descriptions = descriptions.map((d) =>
            d.id === id ? { ...d, state: newState } : d,
        );
    }

    function editAsset(id: number, type: "headline" | "description") {
        // Placeholder for edit functionality
        alert(`Edit ${type} #${id}`);
    }

    // AI Generation State
    let isGenerating = false;
    let generationError: string | null = null;
    let landingPageUrl = "";
    let targetKeywords = "Marketing, Automation, SaaS";

    async function generateWithAI() {
        isGenerating = true;
        generationError = null;

        try {
            const response = await fetch(
                "http://localhost:8000/campaigns/generate-assets",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        landing_page_url:
                            landingPageUrl || "https://example.com",
                        target_keywords: targetKeywords
                            .split(",")
                            .map((k) => k.trim()),
                        brand_voice: "professional",
                        language: "de",
                    }),
                },
            );

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();

            if (data.error) {
                throw new Error(data.message || data.error);
            }

            // Populate headlines
            headlines = data.headlines.map((text: string, index: number) => ({
                id: index + 1,
                text,
                state: "neutral" as AssetState,
            }));

            // Populate descriptions
            descriptions = data.descriptions.map(
                (text: string, index: number) => ({
                    id: headlines.length + index + 1,
                    text,
                    state: "neutral" as AssetState,
                }),
            );
        } catch (error) {
            generationError =
                error instanceof Error ? error.message : "Unknown error";
            console.error("Generation failed:", error);
        } finally {
            isGenerating = false;
        }
    }

    $: selectedHeadlines = headlines.filter(
        (h) => h.state === "selected",
    ).length;
    $: selectedDescriptions = descriptions.filter(
        (d) => d.state === "selected",
    ).length;
</script>

<div
    class="h-screen flex flex-col bg-imap-bg overflow-hidden text-imap-text font-sans"
>
    <Header />

    <!-- Main Content Area (Dashboard Grid) -->
    <main
        class="flex-1 w-full h-full grid grid-cols-[300px_1fr_300px] gap-0 overflow-hidden"
    >
        <!-- Zone 1: Strategy Briefing -->
        <aside class="bg-gray-800/30 border-r border-white/5 p-6 flex flex-col">
            <h2 class="text-white font-semibold mb-4 flex items-center gap-2">
                <span class="w-1 h-6 bg-imap-primary block"></span>
                Strategy Briefing
            </h2>
            <div
                class="flex-1 bg-white/5 p-4 text-gray-300 text-sm overflow-y-auto"
            >
                <p class="mb-4">
                    <strong>Campaign Goal:</strong><br />
                    Increase brand awareness for Q4 product launch.
                </p>
                <p class="mb-4">
                    <strong>Key Message:</strong><br />
                    "Innovation meets reliability."
                </p>
                <p>
                    <strong>Audience:</strong><br />
                    Tech-savvy professionals, aged 25-45.
                </p>
            </div>
        </aside>

        <!-- Zone 2: Asset Workspace -->
        <section
            class="bg-imap-bg p-8 flex flex-col relative w-full h-full overflow-hidden"
        >
            <!-- Background Gradient -->
            <div
                class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-white/5 via-transparent to-transparent pointer-events-none"
            ></div>

            <header class="mb-6 z-10 shrink-0">
                <h1 class="text-2xl text-white font-bold mb-1">
                    Asset Selection
                </h1>
                <p class="text-gray-400 text-sm mb-4">
                    Click tiles to cycle through states: Neutral → Selected →
                    Rejected
                </p>

                <!-- AI Generation Controls -->
                <div class="bg-black/40 border border-white/10 p-4 space-y-3">
                    <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label class="text-gray-400 text-xs mb-1 block"
                                >Landing Page URL</label
                            >
                            <input
                                type="text"
                                bind:value={landingPageUrl}
                                placeholder="https://example.com"
                                class="w-full bg-white/5 border border-white/10 px-3 py-2 text-white text-sm focus:border-imap-primary outline-none"
                            />
                        </div>
                        <div>
                            <label class="text-gray-400 text-xs mb-1 block"
                                >Target Keywords (comma-separated)</label
                            >
                            <input
                                type="text"
                                bind:value={targetKeywords}
                                placeholder="Marketing, Automation, SaaS"
                                class="w-full bg-white/5 border border-white/10 px-3 py-2 text-white text-sm focus:border-imap-primary outline-none"
                            />
                        </div>
                    </div>

                    <div class="flex items-center gap-3">
                        <button
                            on:click={generateWithAI}
                            disabled={isGenerating}
                            class="px-6 py-2 bg-imap-primary hover:bg-imap-primary-hover text-white font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                        >
                            {#if isGenerating}
                                <svg
                                    class="animate-spin h-4 w-4"
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
                                Generating...
                            {:else}
                                ✨ Generate with AI
                            {/if}
                        </button>

                        {#if generationError}
                            <span class="text-red-400 text-sm"
                                >{generationError}</span
                            >
                        {/if}
                    </div>
                </div>
            </header>

            <!-- 2-Column Grid: Headlines | Descriptions -->
            <div class="flex-1 grid grid-cols-2 gap-8 z-10 overflow-hidden">
                <!-- Headlines Column -->
                <div class="flex flex-col">
                    <h3
                        class="text-white font-semibold mb-4 flex items-center gap-2"
                    >
                        <span class="w-1 h-5 bg-imap-primary block"></span>
                        Headlines
                    </h3>
                    <div class="flex-1 overflow-y-auto space-y-3 pr-2">
                        {#each headlines as headline}
                            <AssetTile
                                text={headline.text}
                                state={headline.state}
                                onStateChange={(newState) =>
                                    updateHeadlineState(headline.id, newState)}
                                onEdit={() =>
                                    editAsset(headline.id, "headline")}
                            />
                        {/each}
                    </div>
                </div>

                <!-- Descriptions Column -->
                <div class="flex flex-col">
                    <h3
                        class="text-white font-semibold mb-4 flex items-center gap-2"
                    >
                        <span class="w-1 h-5 bg-imap-primary block"></span>
                        Descriptions
                    </h3>
                    <div class="flex-1 overflow-y-auto space-y-3 pr-2">
                        {#each descriptions as description}
                            <AssetTile
                                text={description.text}
                                state={description.state}
                                onStateChange={(newState) =>
                                    updateDescriptionState(
                                        description.id,
                                        newState,
                                    )}
                                onEdit={() =>
                                    editAsset(description.id, "description")}
                            />
                        {/each}
                    </div>
                </div>
            </div>

            <!-- Counter Bar -->
            <div class="mt-6 z-10 shrink-0">
                <div
                    class="bg-black/40 border border-white/10 p-4 flex justify-between items-center"
                >
                    <div class="flex gap-8">
                        <div>
                            <span class="text-gray-400 text-sm"
                                >Headlines Selected:</span
                            >
                            <span
                                class="ml-2 text-imap-primary font-bold text-lg"
                                >{selectedHeadlines}</span
                            >
                        </div>
                        <div>
                            <span class="text-gray-400 text-sm"
                                >Descriptions Selected:</span
                            >
                            <span
                                class="ml-2 text-imap-primary font-bold text-lg"
                                >{selectedDescriptions}</span
                            >
                        </div>
                    </div>
                    <button
                        class="px-6 py-2 bg-imap-primary hover:bg-imap-primary-hover text-white font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        disabled={selectedHeadlines === 0 ||
                            selectedDescriptions === 0}
                    >
                        Push to Google Ads
                    </button>
                </div>
            </div>
        </section>

        <!-- Zone 3: Targeting & Keywords -->
        <aside class="bg-gray-800/30 border-l border-white/5 p-6 flex flex-col">
            <h2 class="text-white font-semibold mb-4 flex items-center gap-2">
                <span class="w-1 h-6 bg-imap-primary block"></span>
                Targeting
            </h2>
            <div class="flex-1 space-y-4 overflow-y-auto">
                <!-- Keywords Panel -->
                <div class="bg-white/5 p-4 border border-white/5">
                    <h3
                        class="text-gray-400 text-xs uppercase tracking-wider font-bold mb-3"
                    >
                        Keywords
                    </h3>
                    <div class="flex flex-wrap gap-2">
                        <span
                            class="px-2 py-1 bg-black/40 text-gray-300 text-xs border border-white/10"
                            >SaaS</span
                        >
                        <span
                            class="px-2 py-1 bg-black/40 text-gray-300 text-xs border border-white/10"
                            >Marketing</span
                        >
                        <span
                            class="px-2 py-1 bg-black/40 text-gray-300 text-xs border border-white/10"
                            >Automation</span
                        >
                    </div>
                </div>

                <!-- Audience Panel -->
                <div class="bg-white/5 p-4 border border-white/5">
                    <h3
                        class="text-gray-400 text-xs uppercase tracking-wider font-bold mb-3"
                    >
                        Demographics
                    </h3>
                    <ul class="text-sm text-gray-300 space-y-2">
                        <li class="flex justify-between">
                            <span>Age:</span>
                            <span class="text-white">25 - 45</span>
                        </li>
                        <li class="flex justify-between">
                            <span>Location:</span>
                            <span class="text-white">DACH</span>
                        </li>
                    </ul>
                </div>
            </div>
        </aside>
    </main>
</div>
