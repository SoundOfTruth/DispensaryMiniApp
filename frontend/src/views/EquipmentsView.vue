<template>
  <div>
    <div class="equipment-type">Рентгенсистемы</div>
    <div class="equipment">
      <img src="/src/images/test.jpg">
      <div class="name">Рентгенодиагностический комплекс на 3 рабочих места СУР</div>
    </div>
  </div>
</template>


<style lang="scss" scoped>
.equipment-type{
  font-weight: 500;
  font-size: 140%;
  padding-bottom: 20px;
}
img{
  width: 292px;
  height: 270px;
  max-width: 40vw;
  max-height: 40vw;
}
.equipment{
  display: flex;
  background: white;
  align-items: center;
  gap: 10px;
  .name{
    font-size: clamp(75%, 3.7vw, 110%);
    padding-right: 3px;
  }
}
</style>