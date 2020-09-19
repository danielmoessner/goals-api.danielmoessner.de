<template>
  <formulate-form v-bind:name="name" v-on:submit="submit" v-model="formdata">
    <formulate-input
      name="name"
      type="text"
      v-bind:label="label"
      validation="required"
    ></formulate-input>
    <formulate-input
      name="activate"
      type="hidden"
      v-bind:value="this.lastmonday"
    ></formulate-input>
    <formulate-input
      name="deadline"
      type="hidden"
      v-bind:value="this.nextmonday"
    ></formulate-input>
    <formulate-input type="submit" label="Add"></formulate-input>
  </formulate-form>
</template>

<script>
module.exports = {
  name: "AddWeekTodoForm.vue",
  mixins: [formulateSubmitMixin],
  props: {
    weeks: {
      type: Number,
      default: 0,
    },
    label: {
      type: String,
      default: "What else is there to be done this week?",
    },
  },
  data: function () {
    return {
      formdata: {},
      url: "/t/api/normal-todos/",
      name: "addweektodo",
    };
  },
  computed: {
    lastmonday: function () {
      let date = new Date();
      date.setHours(0, 0, 0, 0);
      date.setDate(date.getDate() - ((date.getDay() + 6) % 7));
      date.setDate(date.getDate() + 7 * this.weeks);
      return date;
    },
    nextmonday: function () {
      let date = new Date();
      date.setHours(0, 0, 0, 0);
      date.setDate(this.lastmonday.getDate() + 7);
      return date;
    },
  },
  methods: {},
};
</script>
