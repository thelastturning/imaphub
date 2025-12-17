<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import IconImap from "$lib/components/icons/icon_imap.svelte";

    export let path: string[] = ["Hub"];

    const dispatch = createEventDispatcher();

    // Placeholder for "Is Dirty" check - in a real app this would check a store
    let hasUnsavedChanges = false;

    function handleNavigation(targetIndex: number) {
        if (targetIndex === path.length - 1) return; // Clicked current page

        if (hasUnsavedChanges) {
            // In the future: proper dialog. For now: browser confirm.
            if (!confirm("You have unsaved changes. Discard them?")) {
                return;
            }
        }

        // Logic to navigate based on Breadcrumb.
        // Assuming "Hub" is root #/
        // "CampaignWizard" is #/wizard
        // This is a bit hardcoded for the demo, but flexible enough for now.
        const segment = path[targetIndex];

        if (segment === "Hub") {
            window.location.hash = "/";
        } else if (segment === "CampaignWizard") {
            window.location.hash = "/wizard";
        }
        // Add other mappings as needed
    }
</script>

<header class="w-full">
    <!-- Main Header Bar -->
    <div class="bg-imap-dark flex flex-col w-full">
        <div class="px-8 py-4 flex justify-between items-center">
            <!-- Left: Logo & Breadcrumbs -->
            <div class="flex items-center gap-12">
                <!-- Logo -->
                <div
                    class="select-none cursor-pointer h-5 w-[100px] flex items-center"
                    on:click={() => handleNavigation(0)}
                >
                    <IconImap class="h-full w-auto text-white" />
                </div>

                <!-- Breadcrumbs -->
                <nav
                    class="flex items-center text-sm font-medium tracking-wide"
                >
                    {#each path as segment, index}
                        <div class="flex items-center">
                            {#if index > 0}
                                <span class="mx-3 text-gray-500">/</span>
                            {/if}

                            <!-- Clickable Segment -->
                            <button
                                class="transition-colors duration-200
                                       {index === path.length - 1
                                    ? 'text-white border-b border-imap-accent pb-0.5'
                                    : 'text-gray-400 hover:text-white'}"
                                on:click={() => handleNavigation(index)}
                            >
                                {segment}
                            </button>
                        </div>
                    {/each}
                </nav>
            </div>

            <!-- Right: User Profile (Placeholder) -->
            <div class="flex items-center gap-4">
                <div
                    class="w-10 h-10 rounded-full bg-cover bg-center border border-white/20 relative overflow-hidden group cursor-pointer"
                >
                    <!-- Placeholder Avatar -->
                    <img
                        src="https://ui-avatars.com/api/?name=Fabian+H&background=random&color=fff"
                        alt="User Profile"
                        class="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity"
                    />
                </div>
            </div>
        </div>

        <!-- Separator Line -->
        <div
            class="w-full h-[1px] bg-imap-accent shadow-[0_0_8px_rgba(160,240,195,0.4)]"
        ></div>
    </div>
</header>
