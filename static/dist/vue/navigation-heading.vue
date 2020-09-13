<template>
<li class="my-px">
    <span class="flex font-medium text-sm text-gray-400 px-4 mt-6 mb-2 uppercase" v-html="heading"></span>
</li>
</template>

<script>
module.exports = {
  name: "NavigationHeading",
  props: {
    heading: String
  }
}
</script>