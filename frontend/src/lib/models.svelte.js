/**
 * Reactive Data Models for Svelte 5 (Runes)
 * 
 * Implements "Deep Reactivity" pattern for high-performance Asset workspace.
 */

export class Asset {
    // Rune Properties (Fine-grained reactivity)
    text = $state("");
    type = $state("TEXT");
    pinned = $state(null); // 'HEADLINE_1', 'HEADLINE_2', etc. or null
    id = $state("");

    // Hash is derived, but for now we store it if passed
    hash = $state("");

    constructor(data = {}) {
        this.text = data.text || "";
        this.type = data.type || "TEXT";
        this.pinned = data.pinned || null;
        this.id = data.id || crypto.randomUUID();
        this.hash = data.hash || "";
    }
}

export class AdGroup {
    name = $state("");
    id = $state("");
    headlines = $state([]); // Array of Asset
    descriptions = $state([]); // Array of Asset

    constructor(data = {}) {
        this.name = data.name || "";
        this.id = data.id || crypto.randomUUID();

        // Hydrate arrays with Reactive Asset instances
        this.headlines = (data.headlines || []).map(h => new Asset(h));
        this.descriptions = (data.descriptions || []).map(d => new Asset(d));
    }
}
