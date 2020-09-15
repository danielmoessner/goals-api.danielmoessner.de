<template>
  <div class="flex items-stretch border rounded-lg mb-2 last:mb-0 w-full justify-between bg-white h-12">
    <div class="flex items-center pl-4 w-9/12">
      <input v-on:change="change" v-model="checked" name="completed" value="true"
             class="w-4 h-4 mr-3 cursor-pointer flex-shrink-0" type="checkbox">
      <div class="flex flex-col max-w-full">
        <span class="block text-gray-800 leading-tight truncate" v-html="todo.name"></span>
        <span class="block text-xs text-gray-800 leading-tight"
              v-bind:class="{ 'text-red-500': timeToDeadlineSeconds < 0 }" v-html="timeToDeadline"
              v-if="timeToDeadline"></span>
      </div>
    </div>
    <navigation-button v-bind:text="'Open'" v-bind:link="todo.detail_url"></navigation-button>
  </div>
</template>

<script type="module">
module.exports = {
  name: "ToDo",
  props: {
    todo: Object
  },
  data: function () {
    return {
      checked: this.todo.status === 'DONE'
    }
  },
  components: {
    'navigation-button': httpVueLoader('/static/vue/navigation-button.vue')
  },
  computed: {
    timeToDeadlineSeconds() {
      if (this.todo.status !== 'ACTIVE')
        return 0;
      return (Date.parse(this.todo.deadline) - new Date()) / 1000
    },
    timeToDeadline: function () {
      if (this.todo.status !== 'ACTIVE')
        return "";
      let delta = this.timeToDeadlineSeconds
      let timeToDeadline = delta < 0 ? 'Overdue: ' : ''
      // calculate (and subtract) whole days
      let days = Math.floor(delta / 86400);
      delta -= days * 86400;
      // calculate (and subtract) whole hours
      let hours = Math.floor(delta / 3600) % 24;
      delta -= hours * 3600;
      // calculate (and subtract) whole minutes
      let minutes = Math.floor(delta / 60) % 60;
      delta -= minutes * 60;
      // return human readable time to deadline
      timeToDeadline += days > 0 ? days + 'd ' : ''
      timeToDeadline += hours > 0 ? hours + 'h ' : ''
      timeToDeadline += minutes > 0 ? minutes + 'min ' : ''
      timeToDeadline = timeToDeadline.slice(0, -1)
      return timeToDeadline
    }
  },
  methods: {
    change: function (event) {
      fetch(this.todo.url, {
        method: 'PATCH',
        body: JSON.stringify({
          status: this.checked ? 'DONE' : 'ACTIVE'
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
          "X-CSRFTOKEN": this.csrf_token
        }
      })
          .then(response => response.json())
          .then(data => this.$emit('changed', data))
    }
  }
}
</script>
