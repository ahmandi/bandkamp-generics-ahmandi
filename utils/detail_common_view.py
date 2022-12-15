from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from ..users.permissions import IsAccountOwner

class GetDetailView:
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwner]

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        Obtençao de usuário
        """
        model_object = get_object_or_404(self.view_queryset, pk=pk)

        self.check_object_permissions(request, model_object)

        serializer = self.view_serializer(model_object)

        return Response(serializer.data, status.HTTP_200_OK)

class PatchDetailView:
    def update(self, request: Request, pk: int) -> Response:
        """
        Atualização de usuário
        """
        model_object = get_object_or_404(self.view_queryset, pk=pk)

        self.check_object_permissions(request, model_object)

        serializer = self.view_serializer(model_object, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)

class DeleteDetailView:
    def destroy(self, request: Request, pk: int) -> Response:
        """
        Deleçao de usuário
        """
        model_object = get_object_or_404(self.view_queryset, pk=pk)

        self.check_object_permissions(request, model_object)

        model_object.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class OnlyGetDetailView(GetDetailView, APIView):
    def get(self, request: Request, pk:int) -> Response:
        return super().retrieve(request, pk)

class OnlyPatchDetailView(PatchDetailView, APIView):
    def patch(self, request: Request, pk:int) -> Response:
        return super().update(request, pk)

class OnlyDeleteDetailView(GetDetailView, APIView):
    def delete(self, request: Request, pk:int) -> Response:
        return super().destroy(request, pk)
