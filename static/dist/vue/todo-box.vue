<template>
  <general-box v-bind:heading="heading" :style="{ 'height': todosMinHeight }">
    <div>
      <transition-group name="todo" tag="div" class="relative">
        <to-do v-on:changed="todoChanged" v-for="todo in unarchivedTodos" :key="todo.url" v-bind:todo="todo"
               class="todo-item"></to-do>
      </transition-group>
    </div>
  </general-box>
</template>

<script>
module.exports = {
  name: "TodoBox",
  components: {
    'general-box': httpVueLoader('/static/vue/general-box.vue'),
    'to-do': httpVueLoader('/static/vue/to-do.vue')
  },
  props: {
    url: {
      required: true,
      type: String
    },
    heading: {
      required: true,
      type: String
    },
  },
  data: function () {
    return {
      todos: []
    }
  },
  computed: {
    todosMinHeight: function () {
      return String(8 * 56 - 8) + 'px'
      return String(this.unarchivedTodos.length * 56 - 8) + 'px'
    },
    unarchivedTodos: function () {
      return this.todos.filter(todo => !todo.is_archived)
    }
  },
  mounted() {
    fetch(this.url)
        .then(response => response.json())
        .then(data => (this.todos = data))
  },
  methods: {
    todoChanged: function (data) {
      let index = this.todos.findIndex(todo => todo.url === data.url)
      if (index !== -1) {
        this.todos.splice(index, 1, data)
      }
    }
  }
}
</script>
