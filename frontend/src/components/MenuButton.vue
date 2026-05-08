<template>
  <button class="menu-button">
    <span></span>
    <span></span>
    <span></span>
  </button>
</template>

<style lang="scss">
.menu-button {
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 6px;
  padding: 8px;
  span {
    width: 24px;
    height: 2px;
    background: #222;
    display: block;
    transition: all 0.3s black;
  }
}
</style>
