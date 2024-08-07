<!--
* Tencent is pleased to support the open source community by making
* 蓝鲸智云PaaS平台 (BlueKing PaaS) available.
*
* Copyright (C) 2021 THL A29 Limited, a Tencent company.  All rights reserved.
*
* 蓝鲸智云PaaS平台 (BlueKing PaaS) is licensed under the MIT License.
*
* License for 蓝鲸智云PaaS平台 (BlueKing PaaS):
*
* ---------------------------------------------------
* Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
* documentation files (the "Software"), to deal in the Software without restriction, including without limitation
* the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
* to permit persons to whom the Software is furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of
* the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
* THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
* CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
* IN THE SOFTWARE.
-->

<template>
  <ul>
    <li
      v-for="item in spaceList"
      :class="[
        'list-item',
        {
          'is-select': item.space_uid === spaceUid,
        },
      ]"
      :key="item.id"
      @mousedown="handleProjectChange(item)"
    >
      <span class="list-item-left">
        <span
          class="list-item-name"
          v-bk-overflow-tips
          >{{ item.space_name }}</span
        >
        <span
          v-bk-overflow-tips
          :class="`list-item-id ${theme}-item-code`"
        >
          <!-- ({{ item.space_type_id === eTagsType.biz ? `#${item.id}` : (item.space_id || item.space_code)}}) -->
          ({{ `#${item.space_id || item.space_code}` }})
        </span>
      </span>
      <span
        v-if="showTag"
        class="list-item-right"
      >
        <span
          v-for="tag in item.tags"
          :style="{
            ...spaceTypeMap[tag.id][theme],
          }"
          class="list-item-tag"
          :key="tag.id"
        >
          {{ tag.name }}
        </span>
      </span>
    </li>
  </ul>
</template>

<script>
  import navMenuMixin from '@/mixins/nav-menu-mixin';
  import { SPACE_TYPE_MAP } from '@/store/constant';
  import { mapState } from 'vuex';

  import * as authorityMap from '../../common/authority-map';

  export default {
    mixins: [navMenuMixin],
    props: {
      spaceList: {
        type: Array,
        require: true,
      },
      theme: {
        type: String,
        default: 'dark',
      },
    },
    data() {
      return {
        eTagsType: {
          biz: 'bkcc', // 业务,
          paas: 'paas', // 蓝鲸应用
          container: 'bcs', // 蓝鲸容器平台
          research: 'bkci', // 研发项目
          monitor: 'monitor', // 监控空间
        },
      };
    },
    computed: {
      ...mapState(['isExternal']),
      authorityMap() {
        return authorityMap;
      },
      spaceTypeMap() {
        return SPACE_TYPE_MAP;
      },
      showTag() {
        return !this.isExternal;
      },
    },
    watch: {},
    mounted() {},
    methods: {
      handleProjectChange(space) {
        if (!space.permission?.[authorityMap.VIEW_BUSINESS]) return;
        this.$emit('click-menu-item', space);
      },
    },
  };
</script>

<style scoped lang="scss">
  @import '@/scss/space-tag-option';

  .light-item-code {
    color: #c4c6cc;
  }

  .dark-item-code {
    color: #66768e;
  }
</style>
