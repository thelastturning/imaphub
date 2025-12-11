<script lang="ts">
  let count = $state(0);

  function increment() {
    count += 1;
  }
</script>

<main>
  <h1>IMAP CampaignWizard</h1>
  <div class="card">
    <button onclick={increment}>
      count is {count}
    </button>
  </div>
</main>

<style>
  .card {
    padding: 2em;
  }
</style>
