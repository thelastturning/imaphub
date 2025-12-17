import { Asset, AdGroup } from '$lib/models.svelte.js';

export class WizardState {
    // Top-level campaign state
    campaignName = $state("");
    budget = $state(0);
    language = $state("de");
    targetLocations = $state(["Germany", "Austria", "Switzerland"]);
    objective = $state("LEADS");

    adGroups = $state([]); // Array of AdGroup instances

    // UI State
    isGenerating = $state(false);
    generationProgress = $state(0);

    constructor() {
        this.reset();
    }

    reset() {
        this.campaignName = "";
        this.budget = 0;
        this.language = "de";
        this.targetLocations = ["Germany", "Austria", "Switzerland"];
        this.objective = "LEADS";
        this.adGroups = [];
        this.isGenerating = false;
        this.generationProgress = 0;
    }

    addAdGroup(name) {
        const ag = new AdGroup({ name });
        this.adGroups.push(ag);
        return ag;
    }

    /**
     * Updates the full state from an API response (CampaignStructure)
     */
    loadFromStructure(structure) {
        this.campaignName = structure.campaign_name;
        if (structure.budget_recommendation) {
            this.budget = structure.budget_recommendation;
        }
        if (structure.language) {
            this.language = structure.language;
        }
        if (structure.target_locations) {
            this.targetLocations = structure.target_locations;
        }
        this.adGroups = structure.ad_groups.map(agData => {
            const ag = new AdGroup({
                name: agData.name,
                headlines: agData.assets.headlines.map(h => ({ text: h, type: "TEXT" })),
                descriptions: agData.assets.descriptions.map(d => ({ text: d, type: "TEXT" }))
            });
            return ag;
        });
    }
}

// Global Singleton
export const wizardStore = new WizardState();
