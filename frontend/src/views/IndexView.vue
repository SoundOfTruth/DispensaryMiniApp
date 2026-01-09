<template>
  <div class="about">
    <div class="info">
      <div class="title">Полное наименование</div>
      <div class="text">
        БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ ОМСКОЙ ОБЛАСТИ «КЛИНИЧЕСКИЙ
        ОНКОЛОГИЧЕСКИЙ ДИСПАНСЕР»
      </div>
    </div>
    <div class="info">
      <div class="title">Почтовый адрес</div>
      <div class="text">644013, г. Омск, ул. Завертяева, д. 9, к.1.</div>
    </div>
    <div class="info">
      <div class="title">Фактический адрес</div>
      <div class="text">г. Омск, ул. Завертяева, д. 9, к.1.</div>
    </div>
    <div style="position: relative; overflow: hidden">
      <iframe
        src="https://yandex.ru/map-widget/v1/?ll=73.444809%2C55.040125&mode=poi&poi%5Bpoint%5D=73.444243%2C55.040772&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D1356235732&z=10"
        width="560"
        height="400"
        frameborder="1"
        allowfullscreen="true"
        style="position: relative"
      ></iframe>
    </div>
  </div>
</template>

<style scoped>
.about {
  display: flex;
  gap: 10px;
  flex-direction: column;
}
.info .title {
  font-size: 140%;
  font-weight: 500;
}
.info .text {
  font-size: 100%;
}
</style>
