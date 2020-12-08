<template>
  <div id="stream-controls">
    <!-- TOGGLE MENU BUTTON -->
    <div id="toggle-sidebar">
      <img 
        svg-inline
        src="@/assets/ui/burger-menu.svg"
        alt="Backspace"
        @click="showSidebar()"
      >
    </div>

    <!-- PLAY/STOP BUTTON -->
    <div id="stream-start-settings">
      <div v-if="!isAuto">
        <!-- Not streaming -->
        <div
          v-if="!wsStreamState.open"
          id="play-stop-circle"
          @click="startStreamClicked()"
        >
          <RingLoader
            id="loader"
            :loading="wsStreamState.connecting"
            color="#e2dee9"
          />
          <div id="inner-circle" />
        </div>

        <!-- Streaming -->
        <div
          v-else
          id="stop-box"
          @click="stopStreamClicked()"
        >
          <div id="inner-button" />
        </div>
      </div>
    </div>

    <!-- CAMERA FLIP BUTTON-->
    <div id="stream-camera-flip">
      <svg
        v-if="cameraIconActive"
        id="stream-camera-flip-icon"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        @click="flipCameraClicked()"
      >
        <path fill="#fff" fill-rule="evenodfd" d="M14.571 5.33c.71 0 1.286.576 1.286 1.286v.047h3.214c1.066 0 1.929.864 1.929 1.929v8.143a1.928 1.928 0 01-1.929 1.928H4.93A1.928 1.928 0 013 16.735V8.592c0-1.065.863-1.929 1.929-1.929h3.213v-.047c0-.71.576-1.286 1.287-1.286h5.142zm-4.315 3.899a4.004 4.004 0 00-1.857 5.342l.002.003c.014.028.03.054.045.083l-.06 2.107a.413.413 0 00.401.426H8.8a.414.414 0 00.413-.402l.03-1.064a3.988 3.988 0 004.499.704 3.969 3.969 0 002.035-2.287 3.963 3.963 0 00-.042-2.735l.158-2.116a.414.414 0 00-.826-.062l-.071.957a4.005 4.005 0 00-4.74-.956zm4.318 1.753l-1.42-.106a.415.415 0 00-.061.826l1.918.143c.216.656.215 1.36-.016 2.025-.278.8-.85 1.444-1.613 1.813-.763.37-1.623.42-2.424.141a3.146 3.146 0 01-1.255-.808l1.346.038c.227.017.419-.173.426-.401a.414.414 0 00-.402-.426l-1.945-.056a3.174 3.174 0 011.489-4.197 3.174 3.174 0 013.957 1.008z" />
      </svg>
    </div>

    <!-- MODE SWITCH BUTTON -->
    <!-- <div id="switch-container">
      <b-switch
        v-if="switchIconActive"
        v-model="isAuto"
        class="stream-switch"
        size="is-large"
      >
        <p id="auto-mode">A</p>
        <p id="manual-mode">M</p>
      </b-switch>
    </div> -->
  </div>
</template>

<script>
import { RingLoader } from "vue-spinners-css";
import { eventBus } from "@/main";

export default {
  name: "StreamControls",

  components: {
    RingLoader,
  },

  props: {
    wsStreamState: {
      type: Object,
      default () {
        return {
          connecting: false,
          open: false,
          closed: true,
          paused: false,
        };
      },
    },
    isAuto: {
      type: Boolean,
      default: null,
    },
    cameraIconActive: {
      type: Boolean,
      default: true,
    },
    // switchIconActive: {
    //   type: Boolean,
    //   default: false,
    // },
  },

  data () {
    return {};
  },

  methods: {
    showSidebar () {
      document.getElementById("stream-sidebar").style = "left: calc((100% / 3) * 2);";
    },

    // ----

    startStreamClicked () {
      if (!this.wsStreamState.connecting) {
        eventBus.$emit("startStreaming");
      }
    },

    // ----

    stopStreamClicked () {
      eventBus.$emit("stopStreaming");
    },
    
    // ----

    flipCameraClicked () {
      eventBus.$emit("flipCameraEmitted");
    },
  },
};
</script>

<style lang="scss" scoped>
#stream-controls {
  flex: 0 1 auto;
  width: 20%;
  max-height: 426px;
  display: flex;
  flex-direction: column;

  #toggle-sidebar {
    height: 30%;
    display: flex;
    justify-content: center;
    align-items: center;

    svg {
      outline: none;
    }
  }

  #stream-start-settings {
    height: 40%;

    div {
      width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    #play-stop-circle {
      position: relative;
      width: 3.5rem;
      height: 3.5rem;
      background: none;
      border: 5px solid white;
      border-radius: 50%;
      outline: none;
      transition: all 0.5s;

      #loader {
        position: absolute;
        width: calc(100% + 0.75rem) !important;
        height: calc(100% + 0.75rem) !important;
      }

      #inner-circle {
        position: absolute;
        width: calc(100% - 0.75rem);
        height: calc(100% - 0.75rem);
        background: var(--color-white);
        border-radius: 50%;
        outline: none;
        transition: all 0.5s;
      }
    }

    #stop-box {
      position: relative;
      width: 3.5rem;
      height: 3.5rem;
      background: none;
      border: 5px solid white;
      border-radius: 50%;
      outline: none;
      display: flex;
      justify-content: center;
      align-items: center;
      transition: all 0.5s;

      #inner-button {
        width: 1.5rem;
        height: 1.5rem;
        background: var(--color-error);
        border-radius: 20%;
        transition: all 0.5s;
      }
    }
  }

  #stream-camera-flip {
    height: 30%;
    display: flex;
    justify-content: center;
    align-items: center;

    &-icon {
      width: 2.25rem;
      height: 2.25rem;
    }
  }
}

// #switch-container {
//   display: flex;
//   align-items: center;
//   justify-content: center;
//   height: 30%;
// }

// .stream-switch {
//   margin-right: 0;
//   transition: all 500ms;
//   transform: rotate(90deg);
// }

// #manual-mode {
//   position: absolute;
//   bottom: 7px;
//   left: 10.5px;
//   transform: rotate(-90deg);
//   color: var(--color-purple);
//   font-size: 1rem;
//   font-weight: 600;
// }

// #auto-mode {
//   position: absolute;
//   right: 0.6rem;
//   bottom: 7px;
//   left: 24px;
//   transform: rotate(-90deg);
//   color: var(--main-purple-color);
//   font-size: 1rem;
//   font-weight: 600;
// }

// .switch input[type="checkbox"]:checked + .check {
//   background: rgba(255, 255, 255, 0.6) !important;
// }

// .switch input[type="checkbox"]:focus:checked + .check {
//   box-shadow: none;
// }
</style>