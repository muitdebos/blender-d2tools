<template>
  <div class="button">
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped lang="scss">
.button {
  display: flex;
  justify-content: center;
  align-items: center;
  align-self: center;
  padding: 6px 15px;
  font-size: 14px;
  line-height: 1.25;
  border: 1px solid var(--color-border);
  border-bottom-color: var(--color-border-bottom);
  background-color: var(--color-primary-transparent);
  cursor: pointer;
  white-space: nowrap;
  
  &:hover {
    background-color: var(--color-primary-transparent-hover);
  }

  &.small {
    font-size: 12px;
    line-height: 1;
    padding: 5px 10px;
  }

  &.is-disabled {
    pointer-events: none;
    user-select: none;
    opacity: 0.4;
  }
}
</style>
