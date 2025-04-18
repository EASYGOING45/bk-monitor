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
  <div class="expand-view-wrapper">
    <div class="view-tab">
      <span
        :class="{ active: activeExpandView === 'kv' }"
        @click="activeExpandView = 'kv'"
      >
        KV
      </span>
      <span
        :class="{ active: activeExpandView === 'json' }"
        @click="activeExpandView = 'json'"
      >
        JSON
      </span>
    </div>
    <div
      class="view-content kv-view-content"
      v-show="activeExpandView === 'kv'"
    >
      <kv-list
        :data="data"
        :field-list="totalFields"
        :kv-show-fields-list="kvShowFieldsList"
        :list-data="listData"
        :total-fields="totalFields"
        :visible-fields="visibleFields"
        @value-click="
          (type, content, isLink, field, depth) => $emit('value-click', type, content, isLink, field, depth)
        "
      />
    </div>
    <div
      class="view-content json-view-content"
      v-show="activeExpandView === 'json'"
    >
      <JsonFormatWrapper
        :data="jsonShowData"
        :deep="5"
      />
    </div>
  </div>
</template>

<script>
  import { TABLE_LOG_FIELDS_SORT_REGULAR } from '@/common/util';
  import tableRowDeepViewMixin from '@/mixins/table-row-deep-view-mixin';
  import { getFieldNameByField } from '@/hooks/use-field-name';
  import KvList from '../../result-comp/kv-list.vue';

  export default {
    components: {
      KvList,
    },
    mixins: [tableRowDeepViewMixin],
    inheritAttrs: false,
    props: {
      data: {
        type: Object,
        default: () => {},
      },
      listData: {
        type: Object,
        default: () => {},
      },
      kvShowFieldsList: {
        type: Array,
        require: true,
      },
      rowIndex: {
        type: Number,
      },
    },
    data() {
      return {
        activeExpandView: 'kv',
      };
    },
    computed: {
      visibleFields() {
        return this.$store.state.visibleFields ?? [];
      },
      totalFields() {
        return this.$store.state.indexFieldInfo.fields ?? [];
      },
      kvListData() {
        return this.totalFields
          .filter(item => this.kvShowFieldsList.includes(item.field_name))
          .sort((a, b) => {
            const sortA = getFieldNameByField(a, this.$store).replace(TABLE_LOG_FIELDS_SORT_REGULAR, 'z');
            const sortB = getFieldNameByField(b, this.$store).replace(TABLE_LOG_FIELDS_SORT_REGULAR, 'z');
            return sortA.localeCompare(sortB);
          });
      },
      jsonList() {
        if (this.rowIndex === undefined) {
          return this.listData ?? this.data;
        }

        return this.$store.state.indexSetQueryResult?.origin_log_list?.[this.rowIndex] ?? this.listData ?? this.data;
      },
      jsonShowData() {
        return this.kvListData.reduce((pre, cur) => {
          const fieldName = getFieldNameByField(cur, this.$store);
          pre[fieldName] = this.tableRowDeepView(this.jsonList, cur.field_name, cur.field_type) ?? '';
          return pre;
        }, {});
      },
    },
  };
</script>

<style lang="scss" scoped>
  .expand-view-wrapper {
    width: 100%;
    color: #313238;

    .view-tab {
      font-size: 0;
      background-color: #fafbfd;

      span {
        display: inline-block;
        width: 68px;
        height: 26px;
        font-size: 12px;
        line-height: 26px;
        color: var(--table-fount-color);
        text-align: center;
        cursor: pointer;
        background-color: #f5f7fa;
        border: 1px solid #eaebf0;
        border-top: 0;

        &:first-child {
          border-left: 0;
        }

        &.active {
          color: #3a84ff;
          background-color: #fafbfd;
          border: 0;
        }
      }
    }

    .view-content {
      padding: 10px 30px;
      background-color: #fafbfd;

      :deep(.vjs-tree) {
        /* stylelint-disable-next-line declaration-no-important */
        font-size: var(--table-fount-size) !important;

        .vjs-tree-node {
          line-height: 22px;
          .vjs-value {
            &.vjs-value-string {
              white-space: pre-wrap;
            }
          }
        }
      }

      :deep(.kv-content) {
        .bklog-text-segment {
          &.bklog-root-field {
            max-height: fit-content;
          }
        }
      }
    }
  }
</style>
