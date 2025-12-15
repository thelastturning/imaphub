<script lang="ts">
    import Header from "$lib/components/Header.svelte";

    // Dashboard Logic
    let assets = [
        { id: 1, name: "Generic Asset", type: "generic", color: "gray" },
        { id: 2, name: "Approved Image", type: "image", color: "emerald" },
        { id: 3, name: "Rejected Copy", type: "text", color: "rose" },
    ];
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
                class="flex-1 bg-white/5 p-4 rounded-sm text-gray-300 text-sm overflow-y-auto"
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

            <header class="mb-8 flex justify-between items-end z-10 shrink-0">
                <div>
                    <h1 class="text-2xl text-white font-bold mb-1">
                        Asset Workspace
                    </h1>
                    <p class="text-gray-400 text-sm">
                        Drag and drop assets to organize your campaign.
                    </p>
                </div>
                <button
                    class="px-4 py-2 bg-imap-primary hover:bg-imap-primary-hover text-white text-sm font-semibold transition-colors"
                >
                    + New Asset
                </button>
            </header>

            <!-- Canvas / Grid Area -->
            <div
                class="flex-1 grid grid-cols-3 gap-6 auto-rows-min z-10 overflow-y-auto pb-8"
            >
                <!-- Tile 1 -->
                <div
                    class="aspect-square bg-gray-700/50 border border-white/10 hover:border-imap-primary/50 transition-colors p-4 flex flex-col justify-between group cursor-pointer"
                >
                    <div
                        class="h-8 w-8 bg-gray-600 rounded-full flex items-center justify-center text-xs text-white"
                    >
                        #1
                    </div>
                    <span
                        class="text-gray-300 font-medium group-hover:text-white"
                        >Generic Asset</span
                    >
                </div>

                <!-- Tile 2 -->
                <div
                    class="aspect-square bg-emerald-900/20 border border-emerald-500/30 hover:border-emerald-500/60 transition-colors p-4 flex flex-col justify-between group cursor-pointer"
                >
                    <div
                        class="h-8 w-8 bg-emerald-700 rounded-full flex items-center justify-center text-xs text-white"
                    >
                        #2
                    </div>
                    <span class="text-emerald-100 font-medium"
                        >Approved Image</span
                    >
                </div>

                <!-- Tile 3 -->
                <div
                    class="aspect-square bg-rose-900/20 border border-rose-500/30 hover:border-rose-500/60 transition-colors p-4 flex flex-col justify-between group cursor-pointer"
                >
                    <div
                        class="h-8 w-8 bg-rose-700 rounded-full flex items-center justify-center text-xs text-white"
                    >
                        #3
                    </div>
                    <span class="text-rose-100 font-medium">Rejected Copy</span>
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
                <div class="bg-white/5 p-4 rounded-sm border border-white/5">
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
                <div class="bg-white/5 p-4 rounded-sm border border-white/5">
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
