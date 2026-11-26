from rest_framework import serializers

from core.serializer_fields import FieldsRelatedField
from core.serializers import AssignmentNotificationMixin, BaseModelSerializer

from .models import (
    FinancialInstitution,
    RegulatoryObligation,
    RegulatoryReport,
    Regulator,
    SupervisoryFinding,
)


# Regulators
class RegulatorReadSerializer(BaseModelSerializer):
    folder = FieldsRelatedField()
    filtering_labels = FieldsRelatedField(many=True)
    institutions_count = serializers.IntegerField(
        source="institutions.count", read_only=True
    )

    class Meta:
        model = Regulator
        exclude = []


class RegulatorWriteSerializer(BaseModelSerializer):
    class Meta:
        model = Regulator
        exclude = []


# Financial institutions
class FinancialInstitutionReadSerializer(BaseModelSerializer):
    folder = FieldsRelatedField()
    regulators = FieldsRelatedField(many=True)
    owner = FieldsRelatedField(many=True)
    filtering_labels = FieldsRelatedField(many=True)

    class Meta:
        model = FinancialInstitution
        exclude = []


class FinancialInstitutionWriteSerializer(
    AssignmentNotificationMixin, BaseModelSerializer
):
    assignment_notifications = {"owner": "object_assignment"}

    class Meta:
        model = FinancialInstitution
        exclude = []


# Regulatory obligations
class RegulatoryObligationReadSerializer(BaseModelSerializer):
    folder = FieldsRelatedField()
    regulator = FieldsRelatedField()
    institutions = FieldsRelatedField(many=True)
    frameworks = FieldsRelatedField(many=True)
    applied_controls = FieldsRelatedField(many=True)
    evidences = FieldsRelatedField(many=True)
    owner = FieldsRelatedField(many=True)
    filtering_labels = FieldsRelatedField(many=True)

    class Meta:
        model = RegulatoryObligation
        exclude = []


class RegulatoryObligationWriteSerializer(
    AssignmentNotificationMixin, BaseModelSerializer
):
    assignment_notifications = {"owner": "object_assignment"}

    class Meta:
        model = RegulatoryObligation
        exclude = []


# Regulatory reports
class RegulatoryReportReadSerializer(BaseModelSerializer):
    folder = FieldsRelatedField()
    institution = FieldsRelatedField()
    regulator = FieldsRelatedField()
    obligation = FieldsRelatedField()
    evidences = FieldsRelatedField(many=True)
    owner = FieldsRelatedField(many=True)
    filtering_labels = FieldsRelatedField(many=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = RegulatoryReport
        exclude = []


class RegulatoryReportWriteSerializer(AssignmentNotificationMixin, BaseModelSerializer):
    assignment_notifications = {"owner": "object_assignment"}

    class Meta:
        model = RegulatoryReport
        exclude = []


# Supervisory findings
class SupervisoryFindingReadSerializer(BaseModelSerializer):
    folder = FieldsRelatedField()
    institution = FieldsRelatedField()
    regulator = FieldsRelatedField()
    obligation = FieldsRelatedField()
    applied_controls = FieldsRelatedField(many=True)
    evidences = FieldsRelatedField(many=True)
    owner = FieldsRelatedField(many=True)
    filtering_labels = FieldsRelatedField(many=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = SupervisoryFinding
        exclude = []


class SupervisoryFindingWriteSerializer(
    AssignmentNotificationMixin, BaseModelSerializer
):
    assignment_notifications = {"owner": "object_assignment"}

    class Meta:
        model = SupervisoryFinding
        exclude = []
