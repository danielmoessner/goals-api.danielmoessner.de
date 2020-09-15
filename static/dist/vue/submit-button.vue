<template>
  <input
      class="cursor-pointer flex flex-row items-center py-3 pl-6 pr-6 tracking-wide font-bold rounded-lg text-gray-200 hover:bg-blue-900 bg-blue-800 shadow transition duration-100 ease-in-out focus:outline-none focus:shadow-outline"
      type="submit" v-bind:value="text" />
</template>

<script>
module.exports = {
  name: "SubmitButton",
  props: {
    text: {
      type: String,
      default: 'Submit'
    }
  }
}
</script>
