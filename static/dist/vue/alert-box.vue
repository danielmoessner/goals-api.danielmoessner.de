<template>
  <span
    class="text-gray-100 block px-4 py-2 mb-4 bg-green-500 rounded-md block"
    v-bind:class="{ 'bg-green-500': this.success, 'bg-red-500': this.error, 'bg-blue-500': this.info }"
    v-if="message"
    v-html="message"
  ></span>
</template>

<script>
module.exports = {
  name: "AlertBox",
  props: {
    type: {
      type: String,
      default: "SUCCESS",
    },
    message: {
      type: String,
      required: true,
    },
  },
  data: function () {
    return {};
  },
  computed: {
    success: function () {
      return this.type === "SUCCESS";
    },
    info: function () {
      return this.type === "INFO";
    },
    error: function () {
      return this.type === "ERROR";
    },
  },
};
</script>
