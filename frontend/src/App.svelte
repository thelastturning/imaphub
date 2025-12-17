<script lang="ts">
  import { onMount, tick } from "svelte";

  // Import Pages
  import Hub from "./views/hub/Hub.svelte";
  import CampaignWizard from "./views/wizard/CampaignWizard.svelte";
  import NewCampaign from "./views/wizard/NewCampaign.svelte";
  import CampaignOverview from "./views/wizard/CampaignOverview.svelte";
  import Team from "./views/team/Team.svelte";

  // State
  let currentComponent = Hub;

  async function router() {
    const hash = window.location.hash.replace("#", "") || "/";

    // Simple Router Logic
    if (hash === "/wizard") {
      currentComponent = CampaignWizard;
    } else if (hash === "/wizard/new") {
      currentComponent = NewCampaign;
    } else if (hash === "/wizard/overview") {
      currentComponent = CampaignOverview;
    } else if (hash === "/team") {
      currentComponent = Team;
    } else {
      currentComponent = Hub;
    }

    // Force update if needed, mostly Svelte handles this.
    // console.log("Navigated to:", hash);
  }

  onMount(() => {
    router();
    window.addEventListener("hashchange", router);
    return () => {
      window.removeEventListener("hashchange", router);
    };
  });
</script>

<svelte:component this={currentComponent} />
