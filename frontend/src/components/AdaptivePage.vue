<template>
  <div class="container">
    <slot></slot>
  </div>
</template>

<style lang="scss" scoped>
.container {
  padding: 20px 15px;
  display: grid;

  gap: 15px;
  @media (min-width: 900px) {
    grid-template-columns: 2fr 1fr;
  }
}
</style>
