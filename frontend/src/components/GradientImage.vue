<script setup lang="ts">
interface Props {
  imageUrl: string
  alt?: string
  width?: string
  height?: string
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  alt: '',
  width: 'w-10',
  height: 'h-10',
  className: ''
})
</script>

<template>
  <div 
    class="theme-gradient gradient-mask"
    :class="[props.width, props.height, props.className]"
    :style="{ '--mask-image': `url(${props.imageUrl})` }"
  ></div>
</template>

<style scoped>
.gradient-mask {
  mask: var(--mask-image) no-repeat center/contain;
}
</style> 