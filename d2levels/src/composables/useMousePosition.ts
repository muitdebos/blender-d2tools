import { onMounted, onUnmounted, ref, type Ref } from "vue";

type MousePosition = {
  x: Ref<number>,
  y: Ref<number>,
}

export function useMousePosition(transform?: ((pos: MousePosition) => void)): MousePosition {
  const x = ref(0);
  const y = ref(0);

  function onMouseMove(e: MouseEvent) {
    x.value = e.clientX;
    y.value = e.clientY;

    if (transform) {
      transform({ x, y });
    }
  }

  onMounted(() => {
    window.addEventListener("mousemove", onMouseMove, false);
  });

  onUnmounted(() => {
    window.removeEventListener("mousemove", onMouseMove, false);
  });

  return {
    x,
    y
  };
}
