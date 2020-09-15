<template>
  <div class="shadow-sm rounded-lg border-gray-200 flex flex-col items-baseline bg-white overflow-y-scroll">
    <h2 class="text-xl bg-blue-900 text-gray-100 rounded-br-lg rounded-tl-lg px-4 py-2 font-semibold absolute z-10" v-html="heading"></h2>
    <div class="p-4 w-full pt-16">
      <slot></slot>
    </div>
  </div>
</template>

<script>
module.exports = {
  name: 'GeneralBox',
  props: {
    heading: String
  }
};
</script>