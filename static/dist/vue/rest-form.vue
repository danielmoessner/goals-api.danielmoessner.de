<template>
  <form ref="form" v-on:submit="submit">
    <bootstrap-form v-bind:form="form"></bootstrap-form>
    <div class="flex justify-end">
      <submit-button></submit-button>
    </div>
  </form>
</template>

<script>
module.exports = {
  name: 'RestForm',
  components: {
    'submit-button': httpVueLoader('/static/vue/submit-button.vue'),
    'bootstrap-form': httpVueLoader('/static/vue/bootstrap-form.vue')
  },
  props: {
    url: {
      required: true,
      type: String
    },
    method: {
      type: String,
      default: 'PATCH'
    },
    submiturl: {
      required: true,
      type: String
    }
  },
  data: function () {
    return {
      form: ''
    }
  },
  mounted() {
    fetch(this.url)
        .then(response => response.json())
        .then(data => this.form = data.form)
  },
  methods: {
    submit: function (event) {
      event.preventDefault()
      let formData = new FormData(this.$refs.form)
      fetch(this.submiturl, {
        method: this.method,
        body: formData,
        headers: this.headers
      })
          .then(response => response.json())
          .then(data => data.url ? this.$emit('response', data) : this.$emit('error', data))
    }
  }
}
</script>
