<template>
  <a href="#" class="cursor-pointer text-blue-700 hover:text-blue-900 transition ease-in-out duration-100 ml-4"
     v-on:click="submit"
     v-html="text"></a>
</template>

<script>
module.exports = {
  name: 'FormButton',
  props: {
    link: {
      required: true,
      type: String
    },
    text: {
      required: true,
      type: String
    },
    data: {
      type: Object,
      required: true
    },
    method: {
      type: String,
      default: 'PATCH'
    }
  },
  methods: {
    submit: function () {
      fetch(this.link, {
        method: this.method,
        body: JSON.stringify(this.data),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
          "X-CSRFTOKEN": this.csrf_token
        }
      })
          .then(response => response.json())
          .then(data => this.$emit('response', data))
    }
  }
}
</script>