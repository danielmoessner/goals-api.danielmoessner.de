<template>
  <general-box v-bind:heading="heading">
    <div :style="{ 'min-height': todosMinHeight }">
      <transition-group name="todo" tag="div" class="relative">
        <to-do v-on:changed="todoChanged" v-for="todo in doneToDos" :key="todo.url" v-bind:todo="todo"
               class="todo-item"></to-do>
      </transition-group>
    </div>
  </general-box>
</template>

<script>
export default {
  name: "TodoBox",
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
      return String(this.todos.length * 56 - 8) + 'px'
    }
  },
  mounted() {
    fetch(this.url)
        .then(response => response.json())
        .then(data => (this.todos = data))
  },
  methods: {
    todoChanged: function (data) {
      let index = this.toDos.findIndex(todo => todo.url === data.url)
      if (index !== -1) {
        this.toDos.splice(index, 1, data)
      }
    }
  }
}
</script>
