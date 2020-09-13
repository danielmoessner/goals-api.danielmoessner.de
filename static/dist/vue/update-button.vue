<template>
  <a v-bind:href="link"
     class="flex flex-row items-center py-3 pl-5 pr-6 tracking-wide font-bold rounded-lg text-gray-200 hover:bg-blue-900 bg-blue-800 shadow transition duration-100 ease-in-out focus:outline-none focus:shadow-outline">
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
      icon: '<path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />'
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