"""Financial institutions module (RegTech).

Registers the financial institutions an organisation supervises or works with,
their regulators, the regulatory obligations that apply to them, the reports
filed with the regulators and the findings raised in supervisory inspections.
"""

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from auditlog.registry import auditlog

from core.base_models import AutoRefIdMixin, NameDescriptionMixin
from core.models import Actor, AppliedControl, Evidence, FilteringLabelMixin, Framework
from iam.models import FolderMixin


class Sector(models.TextChoices):
    BANKING = "banking", _("Banking")
    CAPITAL_MARKET = "capital_market", _("Capital market")
    INSURANCE = "insurance", _("Insurance")
    PENSIONS = "pensions", _("Pensions")
    PAYMENTS = "payments", _("Payment services")
    AML = "aml", _("Anti-money laundering")
    CYBERSECURITY = "cybersecurity", _("Cybersecurity")
    DATA_PROTECTION = "data_protection", _("Data protection")
    OTHER = "other", _("Other")


class Regulator(AutoRefIdMixin, NameDescriptionMixin, FolderMixin, FilteringLabelMixin):
    """A supervisory or regulatory authority (e.g. central bank, securities commission)."""

    auto_ref_id_prefix = "REG"
    ref_id = models.CharField(max_length=100, blank=True, verbose_name=_("Reference ID"))
    abbreviation = models.CharField(
        max_length=32, blank=True, verbose_name=_("Abbreviation")
    )
    sector = models.CharField(
        max_length=32,
        choices=Sector.choices,
        default=Sector.BANKING,
        verbose_name=_("Sector"),
    )
    legal_basis = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("Legal basis"),
        help_text=_("Law that establishes the regulator and its powers"),
    )
    website = models.URLField(max_length=500, blank=True, verbose_name=_("Website"))
    contact_email = models.EmailField(blank=True, verbose_name=_("Email"))
    contact_phone = models.CharField(max_length=64, blank=True, verbose_name=_("Phone"))

    fields_to_check = ["name"]

    class Meta:
        verbose_name = _("Regulator")
        verbose_name_plural = _("Regulators")
        ordering = ["name"]

    def __str__(self):
        return f"{self.abbreviation} — {self.name}" if self.abbreviation else self.name


class FinancialInstitution(
    AutoRefIdMixin, NameDescriptionMixin, FolderMixin, FilteringLabelMixin
):
    """A licensed financial institution (bank, insurer, pension company...)."""

    class InstitutionType(models.TextChoices):
        BANK = "bank", _("Bank")
        SAVINGS_HOUSE = "savings_house", _("Savings house")
        INSURANCE = "insurance", _("Insurance company")
        REINSURANCE = "reinsurance", _("Reinsurance company")
        INSURANCE_BROKER = "insurance_broker", _("Insurance broker")
        PENSION_COMPANY = "pension_company", _("Pension fund management company")
        INVESTMENT_FUND_COMPANY = (
            "investment_fund_company",
            _("Investment fund management company"),
        )
        BROKERAGE = "brokerage", _("Brokerage house")
        PAYMENT_INSTITUTION = "payment_institution", _("Payment institution")
        E_MONEY = "e_money", _("Electronic money institution")
        FINANCIAL_COMPANY = "financial_company", _("Financial company")
        LEASING = "leasing", _("Leasing company")
        MICROFINANCE = "microfinance", _("Microfinance institution")
        EXCHANGE_OFFICE = "exchange_office", _("Exchange office")
        OTHER = "other", _("Other")

    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        LICENSING = "licensing", _("Licensing in progress")
        SUSPENDED = "suspended", _("Suspended")
        LIQUIDATION = "liquidation", _("In liquidation")
        REVOKED = "revoked", _("License revoked")

    auto_ref_id_prefix = "FI"
    ref_id = models.CharField(max_length=100, blank=True, verbose_name=_("Reference ID"))
    institution_type = models.CharField(
        max_length=40,
        choices=InstitutionType.choices,
        default=InstitutionType.BANK,
        verbose_name=_("Institution type"),
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name=_("Status"),
    )
    regulators = models.ManyToManyField(
        Regulator,
        blank=True,
        related_name="institutions",
        verbose_name=_("Regulators"),
    )
    license_number = models.CharField(
        max_length=100, blank=True, verbose_name=_("License number")
    )
    license_date = models.DateField(null=True, blank=True, verbose_name=_("License date"))
    registration_number = models.CharField(
        max_length=32,
        blank=True,
        verbose_name=_("Registration number"),
        help_text=_("Company registry number (e.g. EMBS)"),
    )
    tax_number = models.CharField(
        max_length=32, blank=True, verbose_name=_("Tax number")
    )
    lei = models.CharField(max_length=20, blank=True, verbose_name=_("LEI"))
    is_systemic = models.BooleanField(
        default=False,
        verbose_name=_("Systemically important"),
    )
    address = models.CharField(max_length=500, blank=True, verbose_name=_("Address"))
    website = models.URLField(max_length=500, blank=True, verbose_name=_("Website"))
    contact_email = models.EmailField(blank=True, verbose_name=_("Email"))
    contact_phone = models.CharField(max_length=64, blank=True, verbose_name=_("Phone"))
    owner = models.ManyToManyField(
        Actor,
        blank=True,
        related_name="financial_institutions",
        verbose_name=_("Owner"),
    )

    fields_to_check = ["name"]

    class Meta:
        verbose_name = _("Financial institution")
        verbose_name_plural = _("Financial institutions")
        ordering = ["name"]


class RegulatoryObligation(
    AutoRefIdMixin, NameDescriptionMixin, FolderMixin, FilteringLabelMixin
):
    """A requirement imposed by a regulator (law, decision, guideline)."""

    class ObligationType(models.TextChoices):
        REPORTING = "reporting", _("Reporting")
        GOVERNANCE = "governance", _("Corporate governance")
        CAPITAL = "capital", _("Capital adequacy")
        LIQUIDITY = "liquidity", _("Liquidity")
        RISK_MANAGEMENT = "risk_management", _("Risk management")
        IT_SECURITY = "it_security", _("Information security")
        OUTSOURCING = "outsourcing", _("Outsourcing")
        BUSINESS_CONTINUITY = "business_continuity", _("Business continuity")
        AML = "aml", _("Anti-money laundering")
        CONSUMER_PROTECTION = "consumer_protection", _("Consumer protection")
        OTHER = "other", _("Other")

    class Frequency(models.TextChoices):
        ONE_TIME = "one_time", _("One time")
        CONTINUOUS = "continuous", _("Continuous")
        DAILY = "daily", _("Daily")
        WEEKLY = "weekly", _("Weekly")
        MONTHLY = "monthly", _("Monthly")
        QUARTERLY = "quarterly", _("Quarterly")
        SEMI_ANNUAL = "semi_annual", _("Semi-annual")
        ANNUAL = "annual", _("Annual")
        AD_HOC = "ad_hoc", _("Ad hoc")

    class Status(models.TextChoices):
        NOT_ASSESSED = "not_assessed", _("Not assessed")
        COMPLIANT = "compliant", _("Compliant")
        PARTIALLY_COMPLIANT = "partially_compliant", _("Partially compliant")
        NON_COMPLIANT = "non_compliant", _("Non compliant")
        NOT_APPLICABLE = "not_applicable", _("Not applicable")

    auto_ref_id_prefix = "OBL"
    ref_id = models.CharField(max_length=100, blank=True, verbose_name=_("Reference ID"))
    regulator = models.ForeignKey(
        Regulator,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="obligations",
        verbose_name=_("Regulator"),
    )
    legal_reference = models.CharField(
        max_length=500,
        blank=True,
        verbose_name=_("Legal reference"),
        help_text=_("Law, decision or guideline, with the article"),
    )
    obligation_type = models.CharField(
        max_length=32,
        choices=ObligationType.choices,
        default=ObligationType.OTHER,
        verbose_name=_("Obligation type"),
    )
    frequency = models.CharField(
        max_length=20,
        choices=Frequency.choices,
        default=Frequency.CONTINUOUS,
        verbose_name=_("Frequency"),
    )
    status = models.CharField(
        max_length=24,
        choices=Status.choices,
        default=Status.NOT_ASSESSED,
        verbose_name=_("Status"),
    )
    effective_date = models.DateField(
        null=True, blank=True, verbose_name=_("Effective date")
    )
    due_date = models.DateField(null=True, blank=True, verbose_name=_("Due date"))
    institutions = models.ManyToManyField(
        FinancialInstitution,
        blank=True,
        related_name="obligations",
        verbose_name=_("Financial institutions"),
    )
    frameworks = models.ManyToManyField(
        Framework,
        blank=True,
        related_name="regulatory_obligations",
        verbose_name=_("Frameworks"),
    )
    applied_controls = models.ManyToManyField(
        AppliedControl,
        blank=True,
        related_name="regulatory_obligations",
        verbose_name=_("Applied controls"),
    )
    evidences = models.ManyToManyField(
        Evidence,
        blank=True,
        related_name="regulatory_obligations",
        verbose_name=_("Evidences"),
    )
    owner = models.ManyToManyField(
        Actor,
        blank=True,
        related_name="regulatory_obligations",
        verbose_name=_("Owner"),
    )

    fields_to_check = ["name"]

    class Meta:
        verbose_name = _("Regulatory obligation")
        verbose_name_plural = _("Regulatory obligations")
        ordering = ["ref_id", "name"]


class RegulatoryReport(
    AutoRefIdMixin, NameDescriptionMixin, FolderMixin, FilteringLabelMixin
):
    """A report an institution must file with (or has filed with) a regulator."""

    class ReportType(models.TextChoices):
        PERIODIC = "periodic", _("Periodic")
        ANNUAL = "annual", _("Annual")
        INCIDENT = "incident", _("Incident notification")
        AUDIT = "audit", _("Audit report")
        SELF_ASSESSMENT = "self_assessment", _("Self-assessment")
        AD_HOC = "ad_hoc", _("Ad hoc request")
        OTHER = "other", _("Other")

    class Status(models.TextChoices):
        PLANNED = "planned", _("Planned")
        IN_PREPARATION = "in_preparation", _("In preparation")
        IN_REVIEW = "in_review", _("In review")
        SUBMITTED = "submitted", _("Submitted")
        ACCEPTED = "accepted", _("Accepted")
        RETURNED = "returned", _("Returned for correction")

    auto_ref_id_prefix = "RPT"
    ref_id = models.CharField(max_length=100, blank=True, verbose_name=_("Reference ID"))
    institution = models.ForeignKey(
        FinancialInstitution,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reports",
        verbose_name=_("Financial institution"),
    )
    regulator = models.ForeignKey(
        Regulator,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports",
        verbose_name=_("Regulator"),
    )
    obligation = models.ForeignKey(
        RegulatoryObligation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports",
        verbose_name=_("Regulatory obligation"),
    )
    report_type = models.CharField(
        max_length=24,
        choices=ReportType.choices,
        default=ReportType.PERIODIC,
        verbose_name=_("Report type"),
    )
    reporting_period = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_("Reporting period"),
        help_text=_("For example Q3 2026 or 2025"),
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNED,
        verbose_name=_("Status"),
    )
    due_date = models.DateField(null=True, blank=True, verbose_name=_("Due date"))
    submitted_on = models.DateField(
        null=True, blank=True, verbose_name=_("Submitted on")
    )
    submission_reference = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Submission reference"),
        help_text=_("Registry or protocol number given by the regulator"),
    )
    evidences = models.ManyToManyField(
        Evidence,
        blank=True,
        related_name="regulatory_reports",
        verbose_name=_("Evidences"),
    )
    owner = models.ManyToManyField(
        Actor,
        blank=True,
        related_name="regulatory_reports",
        verbose_name=_("Owner"),
    )

    fields_to_check = ["name"]

    class Meta:
        verbose_name = _("Regulatory report")
        verbose_name_plural = _("Regulatory reports")
        ordering = ["due_date", "name"]

    @property
    def is_overdue(self) -> bool:
        return bool(
            self.due_date
            and self.status
            not in (self.Status.SUBMITTED, self.Status.ACCEPTED)
            and self.due_date < timezone.localdate()
        )


class SupervisoryFinding(
    AutoRefIdMixin, NameDescriptionMixin, FolderMixin, FilteringLabelMixin
):
    """A finding or measure issued by a regulator after a supervisory inspection."""

    class Severity(models.TextChoices):
        LOW = "low", _("Low")
        MEDIUM = "medium", _("Medium")
        HIGH = "high", _("High")
        CRITICAL = "critical", _("Critical")

    class Status(models.TextChoices):
        OPEN = "open", _("Open")
        IN_REMEDIATION = "in_remediation", _("In remediation")
        REMEDIATED = "remediated", _("Remediated")
        VERIFIED = "verified", _("Verified by regulator")
        CLOSED = "closed", _("Closed")

    auto_ref_id_prefix = "SF"
    ref_id = models.CharField(max_length=100, blank=True, verbose_name=_("Reference ID"))
    institution = models.ForeignKey(
        FinancialInstitution,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="supervisory_findings",
        verbose_name=_("Financial institution"),
    )
    regulator = models.ForeignKey(
        Regulator,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervisory_findings",
        verbose_name=_("Regulator"),
    )
    obligation = models.ForeignKey(
        RegulatoryObligation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervisory_findings",
        verbose_name=_("Regulatory obligation"),
    )
    inspection = models.CharField(
        max_length=300,
        blank=True,
        verbose_name=_("Inspection"),
        help_text=_("Name or number of the on-site or off-site inspection"),
    )
    inspection_date = models.DateField(
        null=True, blank=True, verbose_name=_("Inspection date")
    )
    severity = models.CharField(
        max_length=16,
        choices=Severity.choices,
        default=Severity.MEDIUM,
        verbose_name=_("Severity"),
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name=_("Status"),
    )
    due_date = models.DateField(null=True, blank=True, verbose_name=_("Due date"))
    remediation_plan = models.TextField(
        blank=True, verbose_name=_("Remediation plan")
    )
    applied_controls = models.ManyToManyField(
        AppliedControl,
        blank=True,
        related_name="supervisory_findings",
        verbose_name=_("Applied controls"),
    )
    evidences = models.ManyToManyField(
        Evidence,
        blank=True,
        related_name="supervisory_findings",
        verbose_name=_("Evidences"),
    )
    owner = models.ManyToManyField(
        Actor,
        blank=True,
        related_name="supervisory_findings",
        verbose_name=_("Owner"),
    )

    fields_to_check = ["name"]

    class Meta:
        verbose_name = _("Supervisory finding")
        verbose_name_plural = _("Supervisory findings")
        ordering = ["due_date", "name"]

    @property
    def is_overdue(self) -> bool:
        return bool(
            self.due_date
            and self.status
            not in (self.Status.REMEDIATED, self.Status.VERIFIED, self.Status.CLOSED)
            and self.due_date < timezone.localdate()
        )


common_exclude = ["created_at", "updated_at"]
for _model in (
    Regulator,
    FinancialInstitution,
    RegulatoryObligation,
    RegulatoryReport,
    SupervisoryFinding,
):
    auditlog.register(_model, exclude_fields=common_exclude)
