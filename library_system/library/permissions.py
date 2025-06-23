from rest_framework.permissions import BasePermission, SAFE_METHODS


# Anyone can read but only admin or librarain can modify
class IsAdminLibrarianOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ['admin', 'librarian']




class IsLibrarianUpdate_SelfUpdate(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if view.action in ['me', 'update_me'] and request.method in ['GET', 'PATCH']:
            return True

        # Allow read-only access to admins and librarians
        if request.method in SAFE_METHODS:
            return user.role in ['admin', 'librarian']

        if request.method in ['POST','PUT', 'PATCH', 'DELETE']:
            return user.role in ['admin', 'librarian']

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Users accesing though me and update/me
        if view.action in ['me', 'update_me']:
            if obj.id != user.id:
                return False

            # Cannot update role or rented_books 
            for field in ['role', 'rented_books']:
                if field in request.data:
                    return False

            return True

        if request.method in SAFE_METHODS:
            if user.role == 'member':
                return obj.id == user.id
            return user.role in ['admin', 'librarian']

        if user.role == 'admin':
            return True

        if user.role == 'librarian':
            if request.method in ['PUT', 'PATCH']:
                new_role = request.data.get('role', obj.role)

                # Can't promote anyone to admin
                if new_role == 'admin':
                    return False

                # Can't change role of non-members to something else
                if obj.role != 'member' and new_role != obj.role:
                    return False

                return True

            if request.method == 'DELETE':
                return obj.role == 'member'

        return False
