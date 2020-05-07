#!/usr/bin/env python
# -*- coding: UTF-8 -*-
def front_user(request):
    user_id = request.session.get('user_id')
    context = {}
    if user_id:
        try:
            # user = User.objects.get(pk=user_id)
            context['front_user'] = user_id
        except:
            pass
    return context