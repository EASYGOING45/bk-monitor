# Generated by Django 3.2.15 on 2023-12-29 03:36
from datetime import datetime

import pytz
from django.db import migrations

import bkmonitor.middlewares.source
from constants.common import DutyCategory


def migrate_duty_groups(apps, schema_editor):
    """
    迁移原历史告警组数据
    """
    DutyRule = apps.get_model("bkmonitor", "DutyRule")
    UserGroup = apps.get_model("bkmonitor", "UserGroup")
    DutyArrange = apps.get_model("bkmonitor", "DutyArrange")
    DutyPlan = apps.get_model("bkmonitor", "DutyPlan")
    DutyRuleRelation = apps.get_model("bkmonitor", "DutyRuleRelation")
    group_queryset = UserGroup.objects.filter(need_duty=True)
    migrated_user_group = []
    migrated_duty_arranges = []
    deleted_duty_arranges = []
    duty_rule_relations = []
    for user_group in group_queryset:
        if user_group.duty_rules:
            # 新版本的，忽略
            print("new duty group({}), turn to next one".format(user_group.name))
            continue
        duty_arranges = list(DutyArrange.objects.filter(user_group_id=user_group.id).order_by("order"))

        if not duty_arranges:
            print("empty duty group({}), turn to next one".format(user_group.name))
            continue

        print("start to migrate duty group({})".format(user_group.name))

        category = DutyCategory.HANDOFF if any([d.need_rotation for d in duty_arranges]) else DutyCategory.REGULAR
        duty_rule = DutyRule.objects.create(
            bk_biz_id=user_group.bk_biz_id,
            name=user_group.name,
            labels=["migrate"],
            enabled=True,
            category=category,
            effective_time=datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:00"),
        )
        for arrange in duty_arranges:
            if not all([arrange.duty_time, arrange.duty_users]):
                # 如果没有轮值人和轮值时间为无效内容，可以删除
                deleted_duty_arranges.append(arrange.id)
                continue
            arrange.duty_rule_id = duty_rule.id
            for duty_time in arrange.duty_time:
                # 对历史的的work_time，需要转变为列表
                if isinstance(duty_time["work_time"], str):
                    duty_time["work_time"] = [duty_time["work_time"]]
            migrated_duty_arranges.append(arrange)
        DutyArrange.objects.filter(user_group_id=user_group.id).update(duty_rule_id=duty_rule.id)
        user_group.duty_rules = [duty_rule.id]
        migrated_user_group.append(user_group)
        duty_rule_relations.append(
            DutyRuleRelation(duty_rule_id=duty_rule.id, user_group_id=user_group.id, bk_biz_id=user_group.bk_biz_id)
        )

    if not migrated_user_group:
        print("no duty user group need to migrate!!")
        return
    # 如果有需要迁移修改的，需要更新一下用户组里的duty_rules
    group_names = ",".join([group.name for group in migrated_user_group])
    group_ids = [group.id for group in migrated_user_group]
    print("create duty rule relations for duty groups({})".format(group_names))
    UserGroup.objects.bulk_update(migrated_user_group, fields=["duty_rules"])
    DutyArrange.objects.bulk_update(migrated_duty_arranges, fields=["duty_rule_id", "duty_time"])
    DutyRuleRelation.objects.bulk_create(duty_rule_relations)

    if deleted_duty_arranges:
        print("delete invalid duty_arranges")
        DutyArrange.objects.filter(id__in=deleted_duty_arranges).delete()
    # 历史的轮值规则删除掉
    print("delete history plans of duty group({})".format(group_names))
    DutyPlan.objects.filter(user_group_id__in=group_ids).delete()

    print("migrate duty user group config done!!")


class Migration(migrations.Migration):
    dependencies = [
        ('bkmonitor', '0156_aifeaturesettings'),
    ]

    operations = [
        migrations.RunPython(migrate_duty_groups),
    ]
