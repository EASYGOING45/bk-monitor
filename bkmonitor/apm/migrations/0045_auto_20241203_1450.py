# Generated by Django 3.2.15 on 2024-12-03 06:50

from django.db import migrations, models

from apm.models import ApmTopoDiscoverRule


def update_discover_rules(apps, schema_editor):
    ApmTopoDiscoverRule.init_builtin_config()


class Migration(migrations.Migration):
    dependencies = [
        ("apm", "0044_bcsclusterdefaultapplicationrelation"),
    ]

    operations = [
        migrations.AddField(
            model_name="apmtopodiscoverrule",
            name="type",
            field=models.CharField(
                choices=[("category", "分类规则"), ("system", "系统类型规则"), ("platform", "平台规则"), ("sdk", "SDK 规则")],
                default="category",
                max_length=32,
                verbose_name="规则类型",
            ),
        ),
        migrations.AddField(
            model_name="toponode",
            name="platform",
            field=models.JSONField(null=True, verbose_name="部署平台"),
        ),
        migrations.AddField(
            model_name="toponode",
            name="sdk",
            field=models.JSONField(null=True, verbose_name="上报sdk"),
        ),
        migrations.AddField(
            model_name="toponode",
            name="system",
            field=models.JSONField(null=True, verbose_name="系统类型"),
        ),
        migrations.AlterField(
            model_name="apmtopodiscoverrule",
            name="category_id",
            field=models.CharField(max_length=128, null=True, verbose_name="分类名称"),
        ),
        migrations.AlterField(
            model_name="apmtopodiscoverrule",
            name="endpoint_key",
            field=models.CharField(max_length=255, null=True, verbose_name="接口字段"),
        ),
        migrations.AlterField(
            model_name="apmtopodiscoverrule",
            name="instance_key",
            field=models.CharField(max_length=255, null=True, verbose_name="实例字段"),
        ),
        migrations.AlterField(
            model_name="apmtopodiscoverrule",
            name="predicate_key",
            field=models.CharField(max_length=128, null=True, verbose_name="判断字段"),
        ),
        migrations.AlterField(
            model_name="apmtopodiscoverrule",
            name="topo_kind",
            field=models.CharField(max_length=50, null=True, verbose_name="topo发现类型"),
        ),
        migrations.RunPython(update_discover_rules),
    ]
