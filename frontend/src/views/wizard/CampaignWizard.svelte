<script>
    import Header from "$lib/components/Header.svelte";
    import IconCampaignWizard from "$lib/components/icons/icon_campaignwizard.svelte";
    import IconImap from "$lib/components/icons/icon_imap.svelte";

    const menuItems = [
        {
            title: "Aktionen",
            apps: [
                {
                    name: "Neue Kampagne",
                    component: IconCampaignWizard,
                    path: "#/wizard/new",
                    active: true,
                },
                {
                    name: "Kampagnen-Übersicht",
                    component: IconImap, // Placeholder icon
                    path: "#/wizard/overview",
                    active: true,
                },
                {
                    name: "None",
                    component: null,
                    path: "#",
                    active: false,
                },
            ],
        },
    ];
</script>

<div
    class="min-h-screen bg-imap-dark text-white font-sans flex flex-col relative overflow-hidden"
>
    <!-- Breadcrumb: Hub / CampaignWizard -->
    <Header path={["Hub", "CampaignWizard"]} />

    <main class="flex-1 py-12 pr-12 overflow-y-auto z-10 pl-[180px]">
        <div class="max-w-7xl space-y-12">
            {#each menuItems as category}
                <section>
                    <h2 class="text-xl font-bold mb-3 text-white tracking-wide">
                        {category.title}
                    </h2>
                    <div
                        class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6"
                    >
                        {#each category.apps as app}
                            <a
                                href={app.path}
                                class="aspect-square flex flex-col justify-center items-center transition-all duration-300 border border-transparent group
                                       {app.active
                                    ? 'bg-imap-tile-dark text-white hover:bg-imap-tile-light hover:border-imap-accent hover:scale-[1.02] hover:shadow-[0_4px_20px_rgba(160,240,195,0.2)] cursor-pointer'
                                    : 'bg-imap-tile-dark text-gray-500 opacity-50 cursor-default'}
                                       "
                            >
                                <div
                                    class="mb-6 {app.active
                                        ? 'text-white group-hover:text-imap-accent'
                                        : 'text-gray-500'}"
                                >
                                    {#if app.component}
                                        <svelte:component
                                            this={app.component}
                                            class="w-24 h-24"
                                        />
                                    {:else}
                                        <div
                                            class="w-24 h-24 border-2 border-current rounded-lg flex items-center justify-center opacity-50"
                                        >
                                            <span class="text-4xl font-bold"
                                                >?</span
                                            >
                                        </div>
                                    {/if}
                                </div>
                                <h3
                                    class="text-xl font-normal font-sans tracking-wide"
                                >
                                    {app.name}
                                </h3>
                            </a>
                        {/each}
                    </div>
                </section>
            {/each}
        </div>
    </main>
</div>
