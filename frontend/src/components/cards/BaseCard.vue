<script setup>
defineProps({
  style: {
    type: String,
    required: false,
  },
  error: {
    type: Error,
    required: false,
    default: null,
  },
  // title: {
  //   type: String,
  //   required: false,
  //   default: null,
  // },
  // icon: {
  //   type: String,
  //   required: false,
  //   default: null,
  // },
});
</script>

<template>
  <section
    class="card flex flex-col overflow-hidden"
    :class="[style, { 'bg-gray-200': error }]"
  >
    <slot />
    <!-- <template >
      <h1 v-if="title" class="mb-4 text-1xl text-gray-400 font-semibold mb-2 uppercase">
        <span v-if="icon" class="mdi text-gray-400 mr-1" :class="['mdi-' + icon]" />
        {{ title }}
      </h1>
    </template> -->

    <div
      v-if="error"
      class="h-full px-2 py-4 flex flex-col gap-2 justify-center text-center"
    >
      <span class="mdi mdi-alert-decagram text-gray-400 text-4xl" />
      <!-- <span class="text-lg font-semibold">{{ error }}</span> -->
      <span class="font-medium text-gray-500"> Could not load data</span>
      <span class="text-xs text-gray-400 italic mx-6">{{ error.message }}</span>
    </div>
  </section>
</template>
