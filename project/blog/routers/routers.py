class PostsAndCommentsRouter(object): 
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'post':
            return 'PostsAndComments'
        elif model._meta.app_label == 'comment':
            return 'PostsAndComments'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'post':
            return 'PostsAndComments'
        elif model._meta.app_label == 'comment':
            return 'PostsAndComments'
        return 'default'
    
    #problem
    def allow_relation(self, obj1, obj2, **hints):
        return True