<template>
  <div class="container">
    <slot></slot>
  </div>
</template>

<style lang="scss" scoped>
.container {
  padding-top: 20px;
  padding-inline: 15px;
  display: grid;
  gap: 15px;
  @media (min-width: 900px) {
    grid-template-columns: 8fr 4fr;
  }
}
</style>
