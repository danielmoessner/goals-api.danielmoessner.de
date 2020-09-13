<template>
  <a v-bind:href="link"
     class="flex flex-row items-center py-3 pl-5 pr-6 tracking-wide font-bold rounded-lg text-gray-100 hover:bg-purple-900 bg-purple-800 shadow transition duration-100 ease-in-out focus:outline-none focus:shadow-outline">
    <div class="flex items-center justify-center text-lg text-gray-400 mr-2">
        <svg fill="none"
             stroke-linecap="round"
             stroke-linejoin="round"
             stroke-width="2"
             viewBox="0 0 20 20"
             stroke="currentColor"
             class="h-5 w-5" v-html="icon">
        </svg>
      </div>
    <span class="" v-html="text"></span>
  </a>
</template>

<script>
module.exports = {
  name: 'UpdateButton',
  data: function () {
    return {
      icon: '<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 000 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />'
    }
  },
  props: {
    link: {
      required: true,
      type: String
    },
    text: {
      required: true,
      type: String
    }
  }
}
</script>