<script>
    // Navigation items
    const apps = [
        {
            name: "Campaign Architect",
            path: "#/wizard",
            icon: `<svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="12" y1="18" x2="12" y2="12"></line><line x1="9" y1="15" x2="15" y2="15"></line></svg>`,
            description: "Design, validate and export marketing campaigns.",
        },
        {
            name: "Team Overview",
            path: "#/team",
            icon: `<svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>`,
            description: "Collaborate and manage team resources.",
        },
    ];
</script>

<div
    class="min-h-screen bg-imap-bg text-imap-text font-sans flex flex-col relative overflow-hidden"
>
    <!-- Background Decor -->
    <div
        class="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-imap-primary/20 blur-[120px] rounded-full pointer-events-none opacity-20"
    ></div>

    <header
        class="p-8 border-b border-white/5 flex justify-between items-center z-10 bg-imap-bg/50 backdrop-blur-sm"
    >
        <div class="font-bold text-xl tracking-tight flex items-center gap-3">
            <div
                class="w-8 h-8 bg-gradient-to-br from-imap-primary to-purple-600 rounded-lg flex items-center justify-center text-white font-bold text-lg"
            >
                I
            </div>
            IMAP<span class="text-gray-500 font-normal">Hub</span>
        </div>
        <div class="flex items-center gap-4">
            <div
                class="w-8 h-8 rounded-full bg-gray-800 border border-white/10"
            ></div>
        </div>
    </header>

    <main class="flex-1 flex flex-col items-center justify-center p-8 z-10">
        <div class="max-w-5xl w-full">
            <h1
                class="text-4xl font-bold text-white mb-2 tracking-tight text-center"
            >
                Welcome back, Fabian.
            </h1>
            <p class="text-gray-400 text-lg mb-12 text-center">
                Select an application to begin your work.
            </p>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {#each apps as app}
                    <a
                        href={app.path}
                        class="group bg-gray-800/40 border border-white/5 hover:border-imap-primary/50 hover:bg-gray-800/60 transition-all duration-300 p-8 rounded-xl cursor-pointer flex flex-col items-start text-left shadow-lg hover:shadow-imap-primary/5 hover:-translate-y-1"
                    >
                        <div
                            class="text-gray-400 group-hover:text-imap-primary transition-colors duration-300 mb-6 bg-white/5 p-4 rounded-lg group-hover:bg-imap-primary/10"
                        >
                            {@html app.icon}
                        </div>
                        <h2
                            class="text-xl font-bold text-white mb-2 group-hover:text-imap-primary transition-colors"
                        >
                            {app.name}
                        </h2>
                        <p class="text-gray-400 text-sm leading-relaxed">
                            {app.description}
                        </p>
                    </a>
                {/each}

                <!-- Add New App Placeholder -->
                <div
                    class="border border-dashed border-white/10 rounded-xl p-8 flex flex-col items-center justify-center text-center opacity-50 hover:opacity-100 hover:border-gray-500 transition-all cursor-not-allowed"
                >
                    <div
                        class="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center text-gray-500 mb-4"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="w-6 h-6"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            ><line x1="12" y1="5" x2="12" y2="19"></line><line
                                x1="5"
                                y1="12"
                                x2="19"
                                y2="12"
                            ></line></svg
                        >
                    </div>
                    <span class="text-sm text-gray-500 font-medium"
                        >Add Module</span
                    >
                </div>
            </div>
        </div>
    </main>
</div>
