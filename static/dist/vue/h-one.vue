<template>
  <h1 class="text-5xl font-bold text-blue-900 tracking-tight leading-none mb-6">
    {{ text }}
    <slot></slot>
  </h1>
</template>

<script>
module.exports = {
  name: "HOne",
  props: {
    text: {
      type: String,
      required: true
    }
  }
}
</script>