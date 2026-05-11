<template>
  <div class="page-header">
    <div>
      <p class="page-kicker">{{ kicker }}</p>
      <h2>{{ title }}</h2>
    </div>
    <p class="page-description">{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  kicker: { type: String, default: "" },
  title: { type: String, required: true },
  description: { type: String, default: "" }
});
</script>

