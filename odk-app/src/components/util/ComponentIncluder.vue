<template>
  <component
    :is="componentData.cTag"
    v-bind="componentData.cProps"
    :src="componentData.cSrc ? require(`../../assets/${componentData.cSrc}`) : null"
    :data="componentData.cData"
  >
    <template v-if="typeof componentData.cContent !== 'string'">
      <template v-for="(node, index) in componentData.cContent">
        <template v-if="typeof node === 'object'">
          <component-includer
            :key="index"
            :slot="node.toSlot"
            :component-data="node"
          >
            <template v-if="node.cContent">{{ node.cContent[index] }}</template>
          </component-includer>
        </template>

        <template v-else>{{ node }}</template>
      </template>
    </template>

    <template v-else>{{ componentData.cContent }}</template>
  </component>
</template>

<script>
export default {
  name: "ComponentIncluder",

  props: {
    componentData: {
      type: Object,
      default: () => {},
    },
  },
};
</script>
