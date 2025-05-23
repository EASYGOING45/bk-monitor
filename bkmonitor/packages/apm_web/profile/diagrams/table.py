"""
Tencent is pleased to support the open source community by making 蓝鲸智云 - 监控平台 (BlueKing - Monitor) available.
Copyright (C) 2017-2022 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from dataclasses import dataclass

from apm_web.profile.diagrams.base import FunctionNode, get_handler_by_mapping
from apm_web.profile.diagrams.diff import ProfileDiffer
from apm_web.profile.diagrams.tree_converter import TreeConverter


@dataclass
class TableDiagrammer:
    def draw(self, c: TreeConverter, **options) -> dict:
        handler = get_handler_by_mapping(options)
        nodes = list(c.tree.function_node_map.values())
        # 添加total节点
        total_node = FunctionNode(id="total", value=c.tree.root.value, name="total", filename="", system_name="")
        nodes.append(total_node)
        sort_map = {
            "name": lambda x: x.name,
            "self": lambda x: x.self_time,
            "total": lambda x: x.value,
            "location": lambda x: x.name,
        }

        if options.get("sort"):
            sorted_nodes = self.sorted_node(node_list=nodes, options=options, sort_map=sort_map)
        else:
            # 默认排序
            sorted_nodes = sorted(nodes, key=lambda x: x.name, reverse=True)
        return {
            "table_data": {
                "total": c.tree.root.value,
                "items": [
                    handler({"id": x.id, "name": x.name, "self": x.self_time, "total": x.value}) for x in sorted_nodes
                ],
            }
        }

    @classmethod
    def sorted_node(cls, node_list: list, options: dict, sort_map: dict):
        sort = str(options.get("sort")).lower()
        sort_field = str(sort).replace("-", "")
        if sort and sort in ["-" + key for key in sort_map.keys()]:
            sorted_nodes = sorted(node_list, key=sort_map.get(sort_field), reverse=True)
        elif sort and sort in sort_map.keys():
            sorted_nodes = sorted(node_list, key=sort_map.get(sort_field))
        else:
            sorted_nodes = node_list

        return sorted_nodes

    def diff(self, base_tree_converter: TreeConverter, comp_tree_converter: TreeConverter, **options) -> dict:
        diff_table = ProfileDiffer.from_raw(base_tree_converter, comp_tree_converter).diff_table()
        table_data = []
        handler = get_handler_by_mapping(options)

        miss_value = {"id": "", "value": 0, "self": 0, "name": "", "system_name": "", "filename": ""}
        for node in diff_table.diff_node_map.values():
            table_data.append(
                {
                    **handler(node.default.to_dict()),
                    **node.diff_info,
                    "baseline_node": handler(node.baseline.to_dict() if node.baseline else miss_value),
                    "comparison_node": handler(node.comparison.to_dict() if node.comparison else miss_value),
                }
            )

        # 排序逻辑 对比图 table 数据
        sort_map = {
            "name": lambda x: x["name"],
            "baseline": lambda x: x["baseline"],
            "comparison": lambda x: x["comparison"],
            "location": lambda x: x["name"],
            "diff": lambda x: x["diff"] if x["diff"] is not None else float("-inf"),
        }
        if options.get("sort"):
            sort_table_data = self.sorted_node(node_list=table_data, options=options, sort_map=sort_map)
        else:
            # 默认排序
            sort_table_data = sorted(table_data, key=lambda x: x["name"], reverse=True)

        return {
            "table_data": {
                "items": sort_table_data,
                "baseline_total": max(item["baseline_node"]["value"] for item in sort_table_data),
                "comparison_total": max(item["comparison_node"]["value"] for item in sort_table_data),
                "total": max(item["value"] for item in sort_table_data),
            }
        }
