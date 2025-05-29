from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework import status
from datetime import date, datetime, timedelta
from apps.models import Debt
from apps.serializers import DebtModelSerializer, ContactDebtModelSerializer


@extend_schema(tags=['debt']
               )
class DebtCreateAPIView(CreateAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtModelSerializer
    


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        response_data = {
            "success": True,
            "data" :{
                "debt":data
            }
        }
        headers = self.get_success_headers(serializer.data)
        return Response(response_data,  status=status.HTTP_201_CREATED, headers=headers)





@extend_schema(tags=['debt']
               )
class DebtListAPIView(ListAPIView):
    serializer_class = DebtModelSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Debt.objects.filter(contact_id=pk)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        datas = []
        active_debts_count = 0
        overdue_debts_count = 0
        total_i_owe = 0
        total_they_owe = 0
        data_summary = {}
        for i in data:
            if i.get("is_overdue"):
                active_debts_count +=1
            else:
                overdue_debts_count+=1

            if i.get("is_my_debt"):
                total_i_owe += float(i.get("debt_amount"))
            else:
                total_they_owe += float(i.get("debt_amount"))


            due = i.get("due_date")
            due_date = datetime.fromisoformat(due).date()
            total = due_date-date.today()
            response_data = {
                "success": True,
                "data":{
                "debts": i ,
                "summary":data_summary,
                "total":total.days
            }
            }
            data_summary["total_i_owe"] = total_i_owe
            data_summary["total_they_owe"] = total_they_owe
            data_summary["active_debts_count"] = active_debts_count
            data_summary["overdue_debts_count"] = overdue_debts_count
            datas.append(response_data)

        return Response(datas)


@extend_schema(tags=["debt"])
class ContactDebtListAPIView(ListAPIView):
    serializer_class = ContactDebtModelSerializer


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
        total_i_owe = 0
        total_they_owe = 0
        data_summary = {}
        data = serializer.data

        for i in data:
            if i.get("is_my_debt"):
                total_i_owe += float(i.get("debt_amount"))
            else:
                total_they_owe += float(i.get("debt_amount"))
        data_summary["total_i_owe"] = total_i_owe
        data_summary["total_they_owe"] = total_they_owe
        return Response(data_summary)



