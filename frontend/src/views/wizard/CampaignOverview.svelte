<script>
    import Header from "$lib/components/Header.svelte";
</script>

<div
    class="h-screen flex flex-col bg-imap-dark overflow-hidden text-imap-text font-sans"
>
    <Header path={["Hub", "CampaignWizard", "Overview"]} />

    <main
        class="flex-1 flex flex-col items-center justify-center p-10 text-center"
    >
        <h1 class="text-4xl text-white font-bold mb-4">Taking the Elevator?</h1>
        <p class="text-xl text-gray-400 max-w-2xl">
            Dieses Modul befindet sich derzeit im Aufbau. Bitte nutzen Sie den
            "Neue Kampagne" Wizard, um neue Assets zu generieren.
        </p>
        <div class="mt-12 p-6 border border-dashed border-white/10 rounded-lg">
            <span class="text-imap-primary font-mono animate-pulse"
                >COMING SOON</span
            >
        </div>
    </main>
</div>
