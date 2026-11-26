from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FinancialInstitutionViewSet,
    RegulatoryObligationViewSet,
    RegulatoryReportViewSet,
    RegulatorViewSet,
    SupervisoryFindingViewSet,
)

router = DefaultRouter()
router.register(r"regulators", RegulatorViewSet, basename="regulators")
router.register(
    r"financial-institutions",
    FinancialInstitutionViewSet,
    basename="financial-institutions",
)
router.register(
    r"regulatory-obligations",
    RegulatoryObligationViewSet,
    basename="regulatory-obligations",
)
router.register(
    r"regulatory-reports", RegulatoryReportViewSet, basename="regulatory-reports"
)
router.register(
    r"supervisory-findings",
    SupervisoryFindingViewSet,
    basename="supervisory-findings",
)

urlpatterns = [
    path("", include(router.urls)),
]
