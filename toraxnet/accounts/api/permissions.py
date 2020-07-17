from rest_framework import permissions


class IsHirer(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user.is_hirer


class IsFreelancer(permissions.BasePermission):
    def has_permission(self,request,view):
        return request.user.is_freelancer

class IsOfferHirer(permissions.BasePermission):
    def has_object_permission(self, request,view,obj):
        return request.user.hirer_profile== obj.posted_by