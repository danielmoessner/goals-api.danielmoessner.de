<template>
  <transition name="fade">
    <general-box v-bind:heading="heading">
      <span class="text-gray-100 block px-4 py-2 mb-4 bg-green-500 rounded-md block" v-if="responsetext"
            v-html="responsetext"></span>
      <span class="text-gray-100 block px-4 py-2 mb-4 bg-red-500 rounded-md block" v-if="errortext"
            v-html="errortext"></span>
      <rest-form v-bind:url="url" v-bind:submiturl="submiturl" method="POST"
                 v-on:response="created" v-on:error="error"></rest-form>
    </general-box>
  </transition>
</template>

<script>
module.exports = {
  name: "AddTodoBox",
  components: {
    'general-box': httpVueLoader('/static/vue/general-box.vue'),
    'rest-form': httpVueLoader('/static/vue/rest-form.vue')
  },
  data: function () {
    return {
      responsetext: '',
      errortext: ''
    }
  },
  props: {
    heading: {
      required: true,
      type: String
    },
    url: {
      required: true,
      type: String
    },
    submiturl: {
      required: true,
      type: String
    }
  },
  methods: {
    created: function (data) {
      this.responsetext = "Todo '" + data.name + "' added."
      this.$emit('response', data)
    },
    error: function (data) {
      this.errortext = 'Error'
      for (const [key, value] of Object.entries(data)) {
        this.errortext += '<br>' + key + ': ' + value
      }
    }
  }
}
</script>
