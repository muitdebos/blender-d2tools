import { onBeforeUnmount, onMounted, ref, type Ref, watch, type ComponentPublicInstance } from "vue";

type Vector2 = {
  x: number
  y: number
}
function getDistanceBetweenVector2(a: Vector2, b: Vector2) {
  return Math.hypot((a.x - b.x), (a.y - b.y));
}


export type UseDraggableOptions = {
  mode?: 'xy' | 'x' | 'y'
  requirement?: (drag: UseDraggableEvent) => boolean // Needs to return true to allow dragging
  minDistance?: number // in px, otherwise counts as click
  allowStartBeforeMinDistance?: boolean // If true, allows `startDrag` before minDistance is reached
  delayForDoubleClick?: boolean // If true and `onDoubleClick` callback is set, delays `onClick` to prevent `click, double click` both firing
  clickDelay?: number // Delay in ms to register as click (allows double-click without single click)
  dragDelay?: number // Delay in ms to register as `startDrag`
}

export type UseDraggableEvent = {
  start: { x: number, y: number }
  start_percent: { x: number, y: number }
  end: { x: number, y: number }
  end_percent: { x: number, y: number }
  diff: { x: number, y: number }
  diff_percent: { x: number, y: number }
}

export type UseDraggableCallback = {
  drag: UseDraggableEvent
  element: Ref<HTMLElement | null>
  container: Ref<HTMLElement | null>
  event?: MouseEvent
}

export type UseDraggableCallbacks = {
  onClick?: (DragEvent: UseDraggableCallback) => void
  onDoubleClick?: (DragEvent: UseDraggableCallback) => void
  onCancel?: (DragEvent: UseDraggableCallback) => void
  onDragStart?: (DragEvent: UseDraggableCallback) => void
  onDragMove?: (DragEvent: UseDraggableCallback) => void
  onDragEnd?: (DragEvent: UseDraggableCallback) => void
}

export function useDraggable(element: Ref<ComponentPublicInstance | HTMLElement | null>, container: Ref<ComponentPublicInstance | HTMLElement | null>, callbacks: UseDraggableCallbacks, options?: UseDraggableOptions) {
  const start = { x: 0, y: 0 };
  const start_percent = { x: 0, y: 0 };
  const end = { x: 0, y: 0 };
  const end_percent = { x: 0, y: 0 };
  const diff = { x: 0, y: 0 };
  const diff_percent = { x: 0, y: 0 };

  const _element: Ref<HTMLElement | null> = ref(null);
  const _container: Ref<HTMLElement | null> = ref(null);
  let box: DOMRect = { width: 0, height: 0, x: 0, y: 0, bottom: 0, left: 0, right: 0, top: 0, toJSON: () => '' };
  let _hasEventListeners = false;
  let _dragTimeout: any = null;
  let _clickTimeout: any = null;
  let _doubleClickTimeout: any = null;
  let _isDoubleClicking = false;
  let _hasReachedMinDistance = false;
  let _startedInteractionOnTarget = false;

  // Exposed
  const isInteracting = ref(false); // Dragging with or without meeting requirements
  const isDragging = ref(false); // Dragging and requirements are met

  const opts: UseDraggableOptions = {
    mode: 'xy',
    requirement: () => true,
    minDistance: 10,
    allowStartBeforeMinDistance: true,
    delayForDoubleClick: true,
    clickDelay: 200,
    dragDelay: 200,
    ...options,
  };

  const allowHorizontal = opts.mode === 'xy' || opts.mode === 'x';
  const allowVertical = opts.mode === 'xy' || opts.mode === 'y';

  onMounted(() => {
    window.addEventListener("mousemove", onMouseMove, false);
    window.addEventListener("mouseup", onMouseUp);
  });

  onBeforeUnmount(() => {
    cancelDrag();
    if (_element.value) {
      _hasEventListeners = false;
      _element.value.removeEventListener("mousedown", onMouseDown);
    }
    window.removeEventListener("mousemove", onMouseMove, false);
    window.removeEventListener("mouseup", onMouseUp);
  });

  watch(element, (el) => {
    if (el && !_hasEventListeners) {
      if ((el as any).$el) {
        _element.value = (el as ComponentPublicInstance).$el;
      }
      else {
        _element.value = (el as HTMLElement);
      }

      _hasEventListeners = true;
      _element.value?.addEventListener("mousedown", onMouseDown);
    }
    else if (_hasEventListeners) {
      _hasEventListeners = false;
    }
    else {
      _element.value = null;
    }
  });


  watch(container, (el) => {
    if (el) {
      if ((el as any).$el) {
        _container.value = (el as ComponentPublicInstance).$el;
      }
      else {
        _container.value = (el as HTMLElement);
      }
    }
    else {
      _container.value = null;
    }
  });

  function onMouseDown(e: MouseEvent) {
    if (_dragTimeout) {
      clearTimeout(_dragTimeout);
    }

    if (_container.value) {
      box = _container.value.getBoundingClientRect();
    }

    _hasReachedMinDistance = false;
    setBlockUserSelect(true);
    _startedInteractionOnTarget = true;

    // Handle double-clicks
    if (_doubleClickTimeout) {
      _isDoubleClicking = true;
      clearTimeout(_doubleClickTimeout);
      _doubleClickTimeout = null;
    }
    else {
      _doubleClickTimeout = setTimeout(() => {
        _doubleClickTimeout = null;
      }, opts.clickDelay);
    }
    
    // Handle drag start conditions
    _dragTimeout = setTimeout(() => {
      _dragTimeout = null;
      if (opts.requirement?.(getCallbackValues().drag)) {
        startDrag(e.clientX, e.clientY);
      }
      else {
        cancelDrag();
      }
    }, opts.dragDelay);
  }

  function onMouseMove(e: MouseEvent) {
    if (isInteracting.value) {
      moveDrag(e.clientX, e.clientY);
    }
  }

  function onMouseUp(e: MouseEvent) {
    // If mouseUp before drag starts, click
    if (_dragTimeout) {
      isInteracting.value = true;
      click(e.clientX, e.clientY, e);
      clearTimeout(_dragTimeout);
      return;
    }

    endDrag(e.clientX, e.clientY);
  }

  function startDrag(x: number, y: number, e?: MouseEvent) {
    isInteracting.value = true;
    
    if (allowHorizontal) {
      start.x = x - box.x;
      start_percent.x = start.x / box.width;
      end.x = start.x;
      end_percent.x = start_percent.x;
      diff.x = 0;
      diff_percent.x = 0;
    }

    if (allowVertical) {
      start.y = y - box.y;
      start_percent.y = start.y / box.height;
      end.y = start.y;
      end_percent.y = start_percent.y;
      diff.y = 0;
      diff_percent.y = 0;
    }

    if (opts.allowStartBeforeMinDistance) {
      isDragging.value = true;
      callbacks.onDragStart?.(getCallbackValues(e));
    }
  }

  function moveDrag(x: number, y: number, e?: MouseEvent) {
    if (isInteracting.value) {
      if (allowHorizontal) {
        end.x = x - box.x;
        end_percent.x = end.x / box.width;
        diff.x = end.x - start.x;
        diff_percent.x = (end.x - start.x) / box.width;
      }

      if (allowVertical) {
        end.y = y - box.y;
        end_percent.y = end.y / box.height;
        diff.y = end.y - start.y;
        diff_percent.y = (end.y - start.y) / box.height;
      }

      const callbackValues = getCallbackValues(e);

      // Stop dragging if we get disabled
      if (!opts.requirement?.(callbackValues.drag)) {
        cancelDrag();
        return;
      }

      const distanceToStart = getDistanceBetweenVector2(start, end);
      // Execute "DragStart" if meeting requirements for the first time
      if (!_hasReachedMinDistance && distanceToStart >= (opts.minDistance ?? 10) && !isDragging.value) {
        _hasReachedMinDistance = true;
        if (!opts.allowStartBeforeMinDistance) {
          isDragging.value = true;
          callbacks.onDragStart?.(callbackValues);
        }
      }
      // Disable again if we no longer meet the requirements
      else if (_hasReachedMinDistance && distanceToStart < (opts.minDistance ?? 10) && isDragging.value) {
        _hasReachedMinDistance = false;
        isDragging.value = false;
      }

      // Execute "DragMove"
      if (opts.allowStartBeforeMinDistance || _hasReachedMinDistance) {
        callbacks.onDragMove?.(callbackValues);
      }
    }
  }

  function endDrag(x: number, y: number, e?: MouseEvent) {
    setBlockUserSelect(false);

    if (isInteracting.value) {
      // If drag stops too close to start, behave as click instead
      const distanceToStart = getDistanceBetweenVector2(start, end);
      if (distanceToStart < (opts.minDistance ?? 10)) {
        click(x, y, e);
        return;
      }
      
      moveDrag(x, y);
      isInteracting.value = false;
      isDragging.value = false;
      _startedInteractionOnTarget = false;
      callbacks.onDragEnd?.(getCallbackValues(e));
    }
  }

  function cancelDrag() {
    setBlockUserSelect(false);
    isInteracting.value = false;
    isDragging.value = false;
    _startedInteractionOnTarget = false;

    start.x = start.y = start_percent.x = start_percent.y = 0;
    end.x = end.y = end_percent.x = end_percent.y = 0;
    diff.x = diff.y = diff_percent.x = diff_percent.y = 0;

    callbacks.onCancel?.(getCallbackValues());
  }

  function click(x: number, y: number, e?: MouseEvent) {
    setBlockUserSelect(false);
    isInteracting.value = false;
    isDragging.value = false;

    start.x = x - box.x;
    start.y = y - box.y;
    start_percent.x = start.x / box.width;
    start_percent.y = start.y / box.height;

    end.x = start.x;
    end.y = end.x;
    end_percent.x = start_percent.x;
    end_percent.y = start_percent.y;

    diff.x = diff.y = 0;
    diff_percent.x = diff_percent.y = 0;

    if (_startedInteractionOnTarget) {
      _startedInteractionOnTarget = false;

      if (_isDoubleClicking) {
        _isDoubleClicking = false;
        callbacks.onDoubleClick?.(getCallbackValues(e));
  
        // Prevent second click from counting as single click
        if (_clickTimeout) {
          clearTimeout(_clickTimeout);
          _clickTimeout = null;
        }
      }
      // Prevent first of two clicks from also counting as single click
      else if (opts.delayForDoubleClick && callbacks.onDoubleClick) {
        _clickTimeout = setTimeout(() => {
          _clickTimeout = null;
  
          // If we're still not double clicking, count as single
          if (!_isDoubleClicking) {
            callbacks.onClick?.(getCallbackValues(e));
          }
        }, opts.clickDelay);
      }
      // Single click
      else {
        if (_clickTimeout) {
          clearTimeout(_clickTimeout);
          _clickTimeout = null;
        }
        callbacks.onClick?.(getCallbackValues(e));
      }
    }
  }

  function setBlockUserSelect(state: boolean) {
    if (window?.document?.body) {
      window.document.body.style.userSelect = state ? 'none' : '';
    }
  }

  function getCallbackValues(e?: MouseEvent): UseDraggableCallback {
    return {
      drag: {
        start, start_percent, 
        end, end_percent,
        diff, diff_percent,
      },
      element: _element,
      container: _container,
      event: e,
    };
  }

  return {
    isInteracting,
    isDragging,
  };
}
