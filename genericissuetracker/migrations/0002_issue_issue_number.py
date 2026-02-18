from django.db import migrations, models
import django.db.models.deletion


def backfill_issue_numbers(apps, schema_editor):
    Issue = apps.get_model("genericissuetracker", "Issue")

    current = 1
    for issue in Issue.objects.all().order_by("created_at"):
        issue.issue_number = current
        issue.save(update_fields=["issue_number"])
        current += 1


class Migration(migrations.Migration):

    dependencies = [
        ("genericissuetracker", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="issue",
            name="issue_number",
            field=models.BigIntegerField(
                unique=True,
                null=True,
                db_index=True,
                editable=False,
            ),
        ),
        migrations.RunPython(backfill_issue_numbers),
        migrations.AlterField(
            model_name="issue",
            name="issue_number",
            field=models.BigIntegerField(
                unique=True,
                db_index=True,
                editable=False,
            ),
        ),
    ]

