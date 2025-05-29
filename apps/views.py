from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Debt
from apps.serializers import SummaryModelSerializer




@extend_schema(tags=["debt"])
class SummaryListAPIView(ListAPIView):
    serializer_class = SummaryModelSerializer


    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Debt.objects.filter(contact_id = pk)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        active_debts_count = 0
        overdue_debts_count = 0
        total_i_owe = 0
        total_they_owe = 0
        data_summary = {}
        data = serializer.data

        for i in data:
            if i.get("is_overdue"):
                active_debts_count += 1
            else:
                overdue_debts_count += 1

            if i.get("is_my_debt"):
                total_i_owe += float(i.get("debt_amount"))
            else:
                total_they_owe += float(i.get("debt_amount"))
        data_summary["total_i_owe"] = total_i_owe
        data_summary["total_they_owe"] = total_they_owe
        data_summary["active_debts_count"] = active_debts_count
        data_summary["overdue_debts_count"] = overdue_debts_count
        return Response(data_summary)

